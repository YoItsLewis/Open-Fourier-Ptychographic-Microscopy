################################################
# RELAUNCH AS ROOT USER IF NOT ALREADY + Libraries
################################################
import os, sys

if os.geteuid() != 0:
    print('Not running as root. Restarting with sudo...')
    os.execvp('sudo',['sudo', sys.executable] + sys.argv)

import tkinter as tk
from tkinter import ttk
from rpi_ws281x import PixelStrip, Color
import time
import RPi.GPIO as GPIO
GPIO.setwarnings(False)

################################################
# LED strip configuration
################################################
LED_COUNT = 256        # 16x16 = 256 LEDs
LED_PIN = 18           # GPIO pin (must support PWM! GPIO18 is normally used)
LED_FREQ_HZ = 800000   # LED signal frequency in Hz (usually 800kHz)
LED_DMA = 10           # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255   # Brightness 0-255 [Dark -> Bright]
LED_INVERT = False     # True to invert the signal if required (NPN transistor level shift)
LED_CHANNEL = 0        # 0 or 1 depending on pin (Set to '1' for GPIOs 13, 19, 41, 45 or 53)

# Camera trigger pin (BCM numbering)
CAMERA_TRIGGER_PIN = 16
GPIO.setmode(GPIO.BCM)
GPIO.setup(CAMERA_TRIGGER_PIN, GPIO.OUT)

################################################
# Initialize LED strip
################################################
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

################################################
# Global state
################################################
led_states = [False] * LED_COUNT
led_buttons = []
buttons_by_index = {} # Map LED index to its GUI button

################################################
# Helper functions
################################################
def led_index(row, col):
    """Map (row, col) to 1D index for zig-zag wiring:
    even rows (0,2,4,...14) run right -> left
    odd rows (1,3,5,...13) run left -> right"""
    if row % 2 == 0:
        return row * 16 + (15 - col)
    else:
        return row * 16 + col

def get_color():
    """Return (r,g,b) for current selection.
    Colors can be added here if needed using RGB color code"""
    choice = color_var.get()
    if choice == 'Red':
        return (255, 0, 0)
    elif choice == 'Green':
        return (0, 255, 0)
    elif choice == 'Blue':
        return (0, 0, 255)
    else:
        return (0, 0, 0) # fallback
   
def on_color_change(event=None):
    """Triggered when dropdown selection changes"""
    # No action needed beyond keeping selection; LEDs read via get_color()
    print(f'Color changed to: {color_var.get()}')
        
def get_timing_values():
    """Retrieve exposure time and capture time value inputs from user """
    try:
        exposure = int(exposure_entry.get())
    except ValueError:
        exposure = 100 # fallback default
    try:
        capture = int(capture_entry.get())
    except ValueError:
        capture = 50 # fallback default
    return exposure, capture

def _fmt_secs(s):
    """Return mm:ss"""
    m = int(s // 60)
    s = int(s % 60)
    return f'{m:02d}:{s:02d}'

def _update_status(k, N, elapsed, eta):
    pct = (k / N) * 100 if N else 0
    status_var.set(f'LED {k}/{N} ({pct:5.1f}%) Elapsed: {_fmt_secs(elapsed)} ETA: {_fmt_secs(eta)}')
    progress.configure(maximum=100, value=pct)
    # ensure UI refreshes during long loops
    root.update_idletasks()

# ----- Orientation controls -----
# Set these until GUI matches physical board
ROTATION = 90        # Choose from {0, 90, 180, 270}
FLIP_H = False      # Mirror left-right after rotation
FLIP_V = False      # Mirror top-bottom after rotation

def _apply_orientation(r, c):
    """Rotate then flip a GUI cell (r,c) to physical matrix coordinates"""
    if ROTATION == 0:
        rr, cc = r, c
    elif ROTATION == 90:
        rr, cc = c, 15 - r
    elif ROTATION == 180:
        rr, cc = 15 - r, 15 -c
    elif ROTATION == 270:
        rr, cc = 15 - c, r
    else:
        rr, cc = r, c # fallback
        
    if FLIP_H:
        cc = 15 - cc
    if FLIP_V:
        rr = 15 - rr
    return rr, cc

def gui_to_strip_index(r, c):
    """Map GUI button (r,c) -> physical 1D LED index with orientation and serpentine"""
    rr, cc = _apply_orientation(r, c)
    return led_index(rr, cc) # uses the existing serpentine mapper

################################################
# LED Patterns (index lists)
################################################
centralLED = [135]

Circle3 = [119,120,121,
             136,135,134,
             151,152,153]

Circle9 = [73,72,71,70,69,
             85,86,87,88,89,90,91,
             107,106,105,104,103,102,101,100,99,
             116,117,118,119,120,121,122,123,124,
             139,138,137,136,135,134,133,132,131,
             148,149,150,151,152,153,154,155,156,
             171,170,169,168,167,166,165,164,163,
             181,182,183,184,185,186,187,
             201,200,199,198,197]

Circle15 = [22,23,24,25,26,
               43,42,41,40,39,38,37,36,35,
               51,52,53,54,55,56,57,58,59,60,61,
               77,76,75,74,73,72,71,70,69,68,67,66,65,
               82,83,84,85,86,87,88,89,90,91,92,93,94,
               110,109,108,107,106,105,104,103,102,101,100,99,98,97,96,
               113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,
               142,141,140,139,138,137,136,135,134,133,132,131,130,129,128,
               145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,
               174,173,172,171,170,169,168,167,166,165,164,163,162,161,160,
               178,179,180,181,182,183,184,185,186,187,188,189,190,
               205,204,203,202,201,200,199,198,197,196,195,194,193,
               211,212,213,214,215,216,217,218,219,220,221,
               235,234,233,232,231,230,229,228,227,
               246,247,248,249,250]

CircleDF5ring = [104,103,102,
                   118,122,
                   137,133,
                   150,154,
                   168,167,166]

################################################
# Pattern function
################################################
def run_trigger_pattern(led_list):
    """Sequentially illuminate indices with camera trigger and timing, with progres/ETA"""
    clear_all()
    time.sleep(0.2)
    
    exposure, capture = get_timing_values()
    r,g,b = get_color()
    N = len(led_list)
    
    # init progress
    progress.configure(value=0)
    status_var.set(f'starting... 0/{N}')
    root.update_idletasks()
    
    t0 = time.time()
    for k, idx in enumerate(led_list, start=1):
        # LED ON
        strip.setPixelColor(idx, Color(r, g, b))
        strip.show()
        # CAMERA TRIGGERED
        GPIO.output(CAMERA_TRIGGER_PIN, True)
        time.sleep(exposure/1000.0) # Exposure time
        GPIO.output(CAMERA_TRIGGER_PIN, False)
        # LED OFF
        strip.setPixelColor(idx, Color(0,0,0))
        strip.show()
        time.sleep(capture/1000.0) # Capture time
        # PROGRESS AND ETA
        elapsed = time.time() - t0
        # estimate per-LED time for elapsed so far
        per_led = elapsed / k
        remaining = max(N - k, 0) * per_led
        _update_status(k, N, elapsed, remaining)
    total = time.time() - t0
    status_var.set(f'Imaging complete. {N}/{N} Total: {_fmt_secs(total)}')
    progress.configure(value=100)
    print('Time taken:', round(total, 3), 'seconds')

def run_hold_pattern(led_list):
    """Illuminate indices simultaneously. Waits for user to press 'Clear All'"""
    clear_all()
    time.sleep(0.2)
    r,g,b = get_color()
    for idx in led_list:
        strip.setPixelColor(idx, Color(r, g, b))
        led_states[idx] = True
        # Update the matching GUI button color
        btn = buttons_by_index.get(idx)
        if btn:
            btn.config(bg=f'#{r:02x}{g:02x}{b:02x}')
    strip.show()
        
################################################
# Core functions
################################################
def toggle_led(idx, button):
    """Toggle a single LED on/off abd nirror color on its button"""
    led_states[idx] = not led_states[idx]
    if led_states[idx]:
        r,g,b = get_color()
        strip.setPixelColor(idx, Color(r, g, b))
        # Match button colour to active colour
        button.config(bg=f"#{r:02x}{g:02x}{b:02x}")
    else:
        strip.setPixelColor(idx, Color(0, 0, 0))
        button.config(bg="gray")
    strip.show()

def clear_all():
    """Turn off all LEDs and reset GUI buttons"""
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(0, 0, 0))
        led_states[i] = False
    strip.show()
    for btn in led_buttons:
        btn.config(bg="gray")
    # Use this so camera never sees a 'stuck high' signal, even if a sequence is interrupted
    GPIO.output(CAMERA_TRIGGER_PIN, False) # Ensures camera trigger pin is low

def close_gui():
    """Exit GUI cleanly"""
    clear_all()
    root.destroy()
    GPIO.cleanup()

################################################
# GUI layout: Controls (left) | 16x16 grid (right)
################################################
root = tk.Tk()
root.title("LED Array Controller")
root.geometry('1000x600') # pick window size
# root.minsize does not work
# ~ root.minsize(1000,590) # Set a sensible minimum so functions can't be squashed


# Make a two-column layout (left control panel, right LED grid)
root.columnconfigure(0, weight=1) # left panel fixed
root.columnconfigure(0, weight=1) # grid expands
root.rowconfigure(1, weight=3)

# Left panel (controls)
left = tk.Frame(root, padx=8, pady=8)
left.grid(row=0, column=0, sticky='nswe')
left.rowconfigure(99, weight=1) # keep controls aligned at top

# Right panel (LED grid)
right = tk.Frame(root, padx=8, pady=8)
right.grid(row=0, column=1, sticky='nswe')
right.rowconfigure(0, weight=1)
right.columnconfigure(0, weight=1)


# ----- Left: group controls into labelled sections -----
# Color section
color_group = ttk.LabelFrame(left, text='Color')
color_group.pack(fill='x', pady=(0,8))

# Variable to store current color
color_var = tk.StringVar(value='Red')
# Create Combobox
color_dropdown = ttk.Combobox(color_group, textvariable=color_var, state='readonly', width=12)
color_dropdown['values'] = ('Red', 'Green', 'Blue') # Change if more colors are added
color_dropdown.pack(fill='x', padx=4, pady=4)
color_dropdown.bind('<<ComboboxSelected>>', on_color_change)

# Triggered pattern section
triggered_pattern_group = ttk.LabelFrame(left, text='Triggered Patterns')
triggered_pattern_group.pack(fill='x', pady=(0,8))

tk.Button(triggered_pattern_group, text="Brightfield - 9 LEDs", command=lambda: run_trigger_pattern(Circle3)).pack(fill='x', padx=4, pady=3)
tk.Button(triggered_pattern_group, text="FPM - 69 LEDs", command=lambda: run_trigger_pattern(Circle9)).pack(fill='x', padx=4, pady=3)
tk.Button(triggered_pattern_group, text="FPM - 177 LEDs", command=lambda: run_trigger_pattern(Circle15)).pack(fill='x', padx=4, pady=3)

# Pattern section
hold_pattern_group = ttk.LabelFrame(left, text='Hold Patterns')
hold_pattern_group.pack(fill='x', pady=(0,8))

tk.Button(hold_pattern_group, text="Brightfield", command=lambda: run_hold_pattern(Circle3)).pack(fill='x', padx=4, pady=3)
tk.Button(hold_pattern_group, text="Darkfield", command=lambda: run_hold_pattern(CircleDF5ring)).pack(fill='x', padx=4, pady=3)
# Don't recommend due to high current draw from high number of LEDs in use
# ~ tk.Button(hold_pattern_group, text="Brightfield - Incoherent", command=lambda: run_hold_pattern(Circle15)).pack(fill='x', padx=4, pady=3)

# Timing section
timing_group = ttk.LabelFrame(left, text='Timing')
timing_group.pack(fill='x', pady=(0,8))
# Exposure
row = tk.Frame(timing_group); row.pack(fill='x', padx=4, pady=3)
tk.Label(row, text='Exposure (ms):').pack(side='left')
exposure_entry = tk.Entry(row, width=6); exposure_entry.insert(0,'100')
exposure_entry.pack(side='left', padx=6)
# Capture
row = tk.Frame(timing_group); row.pack(fill='x', padx=4, pady=3)
tk.Label(row, text='Capture (ms):').pack(side='left')
capture_entry = tk.Entry(row, width=6); capture_entry.insert(0,'50')
capture_entry.pack(side='left', padx=16)

# Utilities section
utils_group = ttk.LabelFrame(left, text='Utilities')
utils_group.pack(fill='x', pady=(0,8))
tk.Button(utils_group, text="Clear All", command=clear_all).pack(fill='x', padx=4, pady=3)
tk.Button(utils_group, text="Exit", command=close_gui).pack(fill='x', padx=4, pady=3)

# ----- Status (Bottom-left) -----
status_group = ttk.LabelFrame(left, text='Status')
status_group.pack(fill='x', pady=(0,8))

status_var = tk.StringVar(value='Idle')
status_label = tk.Label(status_group, textvariable=status_var, anchor='w')
status_label.pack(fill='x', padx=4, pady=(4,2))

progress = ttk.Progressbar(status_group, mode='determinate', maximum=100, value=0)
progress.pack(fill='x', padx=4, pady=(0,6))

# ----- Right: 16x16 grid of LED buttons -----
# Frame for LED grid
grid_frame = tk.Frame(right)
grid_frame.grid(row=0, column=0, sticky='nsew')

#weights for resizing - Use if needed
# ~ for r in range(16):
    # ~ grid_frame.rowconfigure(r, weight=1)
# ~ for c in range(16):
    # ~ grid_frame.columnconfigure(c, weight=1)

for r in range(16):
    for c in range(16):
        idx = gui_to_strip_index(r, c) # Orientation-aware index
        text = 'X' if idx == 135 else ''
        btn = tk.Button(grid_frame, width=1, height=1, bg="gray", text=text)
        btn.grid(row=r, column=c, padx=1, pady=1, sticky='nsew')
        btn.config(command=lambda i=idx, b=btn: toggle_led(i, b))
        led_buttons.append(btn)
        buttons_by_index[idx] = btn

################################################
# Run GUI
################################################
root.mainloop()
