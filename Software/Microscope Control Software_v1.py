################################################
# Relaunch as root (keeping X11 env) + grant access
################################################
import os, sys, subprocess, pathlib

# Ensure DISPLAY/XAUTHORITY exist (helps under XRDP)
user_home = str(pathlib.Path.home())
os.environ.setdefault("DISPLAY", os.environ.get("DISPLAY", ":0"))
os.environ.setdefault("XAUTHORITY", os.path.join(user_home, ".Xauthority"))

if os.geteuid() != 0:
    # Allow root to connect to the current X server (run before sudo)
    try:
        subprocess.run(["xhost", "+SI:localuser:root"],
                       check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass

    print("Not running as root. Restarting with sudo -E ...")
    # Re-exec as root, preserving env (incl. DISPLAY/XAUTHORITY)
    os.execvp("sudo", ["sudo", "-E", sys.executable] + sys.argv)

################################################
# Main Libraries
################################################

import tkinter as tk
from tkinter import ttk
from rpi_ws281x import PixelStrip, Color
import time
import RPi.GPIO as GPIO
GPIO.setwarnings(False)

################################################
# LED Strip Configuration
################################################
LED_COUNT = 256        # 16x16 = 256 LEDs
LED_PIN = 18           # GPIO pin (must support PWM! GPIO18 is normally used)
LED_FREQ_HZ = 800000   # LED signal frequency in Hz (usually 800kHz)
LED_DMA = 10           # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255   # Brightness 1-255 [Dark -> Bright]
LED_INVERT = False     # True to invert the signal if required (NPN transistor level shift)
LED_CHANNEL = 0        # 0 or 1 depending on pin (Set to '1' for GPIOs 13, 19, 41, 45 or 53)

# Camera trigger pin (BCM numbering)
CAMERA_TRIGGER_PIN = 16
GPIO.setmode(GPIO.BCM)
GPIO.setup(CAMERA_TRIGGER_PIN, GPIO.OUT, initial=GPIO.LOW)

################################################
# Initialise LED Strip
################################################
strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()
strip.setBrightness(LED_BRIGHTNESS)

################################################
# Stepper Motors (28BYJ-48 - half-step)
################################################
MOTOR1_PINS = [4, 17, 27, 22]    # Z - Motor
MOTOR2_PINS = [10, 9, 11, 0]     # X - Motor
MOTOR3_PINS = [5, 6, 19, 26]     # Y - Motor

for p in MOTOR1_PINS + MOTOR2_PINS + MOTOR3_PINS:
    GPIO.setup(p, GPIO.OUT)
    GPIO.output(p, GPIO.LOW)

# 8-step half-step sequence
SEQ_HALF_FWD = [
    [1,0,0,0],
    [1,1,0,0],
    [0,1,0,0],
    [0,1,1,0],
    [0,0,1,0],
    [0,0,1,1],
    [0,0,0,1],
    [1,0,0,1]]

SEQ_HALF_BWD = list(reversed(SEQ_HALF_FWD))

# 28BYJ-48: 512 cycles * 8 half-steps = 4096 half-steps ≈ 1 output-shaft revolution
STEPS_PER_REV_CYCLES = 512

# Fixed motor timing - change here if needed.
# If motors stall increase to 1.5-2.5 ms
# If motors are smooth or you want to focus on speed, try 0.7-0.8 ms
### DON'T GO BELOW 0.5 ms
MOTOR_STEP_DELAY_MS = 1.0 # ms per half-step (blocking)

def _deenergise(pins):
    for p in pins:
        GPIO.output(p, GPIO.LOW)

def _run_motor_blocking(pins, seq, cycles, delay_ms):
    """Blocking motor move (no threading)."""
    delay = max(0.0005, float(delay_ms)/1000.0)  # safety floor
    for _ in range(int(cycles)):
        for halfstep in range(8):
            for ch in range(4):
                GPIO.output(pins[ch], seq[halfstep][ch])
            time.sleep(delay)
    _deenergise(pins)

################################################
# Global State
################################################
led_states = [False] * LED_COUNT
led_buttons = []
buttons_by_index = {} # Map LED index to its corresponding GUI button

################################################
# Helper Functions
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
    choice = color_var.get()
    if choice == 'Red':
        return (255, 0, 0)
    elif choice == 'Green':
        return (0, 255, 0)
    elif choice == 'Blue':
        return (0, 0, 255)
    elif choice == 'Purple':
        return (128, 0, 128)
    elif choice == 'Orange':
        return (255, 165, 0)
    elif choice == 'Cyan':
        return (0, 255, 255)
    elif choice == 'RGB':
        return (255, 255, 255)
    else:
        return (0, 0, 0) # fallback

def on_color_change(event=None):
    print(f'Color changed to: {color_var.get()}')

def get_timing_values():
    try:
        exposure = int(exposure_entry.get())
    except ValueError:
        exposure = 100
    try:
        capture = int(capture_entry.get())
    except ValueError:
        capture = 10
    return exposure, capture

def _fmt_secs(s):
    m = int(s // 60)
    s = int(s % 60)
    return f'{m:02d}:{s:02d}'

def _update_status(k, N, elapsed, eta):
    pct = (k / N) * 100 if N else 0
    status_var.set(f'LED {k}/{N} ({pct:5.1f}%) Elapsed: {_fmt_secs(elapsed)} ETA: {_fmt_secs(eta)}')
    progress.configure(maximum=100, value=pct)
    root.update_idletasks()

# ----- LED Orientation Controls -----
ROTATION = 90        # {0, 90, 180, 270}
FLIP_H = False
FLIP_V = False

def _apply_orientation(r, c):
    if ROTATION == 0:
        rr, cc = r, c
    elif ROTATION == 90:
        rr, cc = c, 15 - r
    elif ROTATION == 180:
        rr, cc = 15 - r, 15 - c
    elif ROTATION == 270:
        rr, cc = 15 - c, r
    else:
        rr, cc = r, c
    if FLIP_H:
        cc = 15 - cc
    if FLIP_V:
        rr = 15 - rr
    return rr, cc

def gui_to_strip_index(r, c):
    rr, cc = _apply_orientation(r, c)
    return led_index(rr, cc)

# ----- Brightness Controls -----
def _apply_brightness(v: int):
    v = max(1, min(int(v), 255))
    strip.setBrightness(v)
    strip.show()
    return v

def on_brightness_slider(val=None):
    v = int(float(val))
    v = _apply_brightness(v)
    brightness_var.set(v)
    brightness_entry_var.set(str(v))

def on_brightness_entry(_event=None):
    try:
        v = int(brightness_entry_var.get())
    except ValueError:
        v = brightness_var.get()
    v = _apply_brightness(v)
    brightness_var.set(v)
    brightness_entry_var.set(str(v))

def validate_entry(new_val):
    if new_val == '':  # allow temporary blank while typing
        return True
    if new_val.isdigit():
        v = int(new_val)
        return 1 <= v <= 255
    return False

# ----- Stepper Motor Controls -----
def _on_step_combo(_evt=None):
    try:
        selected_cycles_var.set(int(step_combo.get()))
    except ValueError:
        selected_cycles_var.set(128); step_combo.set('128')

def _get_selected_cycles():
    try:
        return int(selected_cycles_var.get())
    except Exception:
        return 128

def _set_coils(pins, pattern_row):
    for ch in range(4):
        GPIO.output(pins[ch], pattern_row[ch])
    
def _run_two_motors_blocking(pinsA, seqA, pinsB, seqB, cycles, delay_ms):
    """ Step two 28BYJ-48 motors in lockstep (blocking, no threads)."""
    delay = max(0.0005, float(delay_ms)/1000.0) # safety floor
    for _ in range(int(cycles)):
        for hs in range(8): # half-step subphase
            _set_coils(pinsA, seqA[hs])
            _set_coils(pinsB, seqB[hs])
            time.sleep(delay)
    _deenergise(pinsA)
    _deenergise(pinsB)

def _move_sel(pins, seq):
    # wrapper uses the combo-selected cycles
    _run_motor_blocking(pins, seq, _get_selected_cycles(), MOTOR_STEP_DELAY_MS)
    
def _move_two_sel(pinsA, seqA, pinsB, seqB):
    # interleaves the half-steps for both motors so they stay in sync with one another
    _run_two_motors_blocking(pinsA, seqA, pinsB, seqB, _get_selected_cycles(), MOTOR_STEP_DELAY_MS)

################################################
# LED Patterns (index lists) 
# TODO: Put your patterns here
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
# Pattern Functions
################################################
def run_trigger_pattern(led_list):
    clear_all()
    time.sleep(0.2)
    exposure, capture = get_timing_values()
    r,g,b = get_color()
    N = len(led_list)
    progress.configure(value=0)
    status_var.set(f'starting... 0/{N}')
    root.update_idletasks()
    t0 = time.time()
    for k, idx in enumerate(led_list, start=1):
        strip.setPixelColor(idx, Color(r, g, b)); strip.show()
        GPIO.output(CAMERA_TRIGGER_PIN, True)
        time.sleep(exposure/1000.0)
        GPIO.output(CAMERA_TRIGGER_PIN, False)
        strip.setPixelColor(idx, Color(0,0,0)); strip.show()
        time.sleep(capture/1000.0)
        elapsed = time.time() - t0
        per_led = elapsed / k
        remaining = max(N - k, 0) * per_led
        _update_status(k, N, elapsed, remaining)
    total = time.time() - t0
    status_var.set(f'Imaging complete. {N}/{N} Total: {_fmt_secs(total)}')
    progress.configure(value=100)
    print('Time taken:', round(total, 3), 'seconds')

def run_hold_pattern(led_list):
    clear_all()
    time.sleep(0.2)
    r,g,b = get_color()
    for idx in led_list:
        strip.setPixelColor(idx, Color(r, g, b))
        led_states[idx] = True
        btn = buttons_by_index.get(idx)
        if btn:
            btn.config(bg=f'#{r:02x}{g:02x}{b:02x}')
    strip.show()

################################################
# Core Functions
################################################
def toggle_led(idx, button):
    led_states[idx] = not led_states[idx]
    if led_states[idx]:
        r,g,b = get_color()
        strip.setPixelColor(idx, Color(r, g, b))
        button.config(bg=f"#{r:02x}{g:02x}{b:02x}")
    else:
        strip.setPixelColor(idx, Color(0, 0, 0))
        button.config(bg="gray")
    strip.show()

def clear_all():
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(0, 0, 0))
        led_states[i] = False
    strip.show()
    for btn in led_buttons:
        btn.config(bg="gray")
    GPIO.output(CAMERA_TRIGGER_PIN, GPIO.LOW)
    for pins in (MOTOR1_PINS, MOTOR2_PINS, MOTOR3_PINS):
        _deenergise(pins)

def close_gui():
    clear_all()
    root.destroy()
    GPIO.cleanup()

##########################################################################
# GUI Layout: [Left LED controls] | [Middle grid+status] | [Right motors]
##########################################################################
root = tk.Tk()
root.title("LED Array Controller")
root.geometry('1300x625')

# 3 columns: left & right fixed-ish, middle expands
root.columnconfigure(0, weight=0, minsize=360)   # LEFT controls
root.columnconfigure(1, weight=0)                # MIDDLE grid+status
root.columnconfigure(2, weight=1, minsize=380)   # RIGHT motors
root.rowconfigure(0, weight=1)

# Left controls panel
left_controls = tk.Frame(root, padx=8, pady=8)
left_controls.grid(row=0, column=0, sticky='nsew')

# Middle panel (grid + status)
center = tk.Frame(root, padx=8, pady=8)
center.grid(row=0, column=1, sticky='nsew')
center.rowconfigure(0, weight=0)   # don't stretch the grid row
center.rowconfigure(1, weight=0)   # keep status natural height
center.columnconfigure(0, weight=1)

# Right motors panel
right_motors = tk.Frame(root, padx=8, pady=8)
right_motors.grid(row=0, column=2, sticky='nw')

# ========= LEFT CONTROLS (pack inside left_controls) =========
# Color
color_group = ttk.LabelFrame(left_controls, text='Color')
color_group.pack(fill='x', pady=(0,8))
color_var = tk.StringVar(value='Red')
color_dropdown = ttk.Combobox(color_group, textvariable=color_var, state='readonly', width=12)
color_dropdown['values'] = ('Red', 'Green', 'Blue', 'Purple', 'Orange', 'Cyan', 'RGB') # Change if more colors are added
color_dropdown.pack(fill='x', padx=4, pady=4)
color_dropdown.bind('<<ComboboxSelected>>', on_color_change)

# Brightness
brightness_group = ttk.LabelFrame(left_controls, text='Brightness')
brightness_group.pack(fill='x', pady=(0,8))
brightness_var = tk.IntVar(value=LED_BRIGHTNESS)
brightness_entry_var = tk.StringVar(value=str(LED_BRIGHTNESS))
row = tk.Frame(brightness_group); row.pack(fill='x', padx=4, pady=4)
brightness_slider = ttk.Scale(row, from_=1, to=255, variable=brightness_var, orient='horizontal', command=on_brightness_slider)
brightness_slider.pack(side='left', fill='x', expand=True)
vcmd = (root.register(validate_entry), '%P')
brightness_entry = ttk.Entry(row, width=5, textvariable=brightness_entry_var, justify='right', validate='key', validatecommand=vcmd)
brightness_entry.pack(side='right', padx=6)
brightness_entry.bind('<Return>', on_brightness_entry)
brightness_entry.bind('<FocusOut>', on_brightness_entry)

# Timing
timing_group = ttk.LabelFrame(left_controls, text='Timing')
timing_group.pack(fill='x', pady=(0,8))
row = tk.Frame(timing_group); row.pack(fill='x', padx=4, pady=3)
tk.Label(row, text='Exposure (ms):').pack(side='left')
exposure_entry = tk.Entry(row, width=6); exposure_entry.insert(0,'100')
exposure_entry.pack(side='left', padx=6)
row = tk.Frame(timing_group); row.pack(fill='x', padx=4, pady=3)
tk.Label(row, text='Capture (ms):').pack(side='left')
capture_entry = tk.Entry(row, width=6); capture_entry.insert(0,'10')
capture_entry.pack(side='left', padx=16)

# Hold patterns
hold_pattern_group = ttk.LabelFrame(left_controls, text='Hold Patterns')
hold_pattern_group.pack(fill='x', pady=(0,8))
tk.Button(hold_pattern_group, text="Brightfield", command=lambda: run_hold_pattern(Circle3)).pack(fill='x', padx=4, pady=3)
tk.Button(hold_pattern_group, text="Darkfield", command=lambda: run_hold_pattern(CircleDF5ring)).pack(fill='x', padx=4, pady=3)

# Triggered patterns
triggered_pattern_group = ttk.LabelFrame(left_controls, text='Triggered Patterns')
triggered_pattern_group.pack(fill='x', pady=(0,8))
tk.Button(triggered_pattern_group, text="Brightfield - 9 LEDs", command=lambda: run_trigger_pattern(Circle3)).pack(fill='x', padx=4, pady=3)
tk.Button(triggered_pattern_group, text="FPM - 69 LEDs", command=lambda: run_trigger_pattern(Circle9)).pack(fill='x', padx=4, pady=3)
tk.Button(triggered_pattern_group, text="FPM - 177 LEDs", command=lambda: run_trigger_pattern(Circle15)).pack(fill='x', padx=4, pady=3)

# Utilities
utils_group = ttk.LabelFrame(left_controls, text='Utilities')
utils_group.pack(fill='x', pady=(0,8))
tk.Button(utils_group, text="Clear All", command=clear_all).pack(fill='x', padx=4, pady=3)
tk.Button(utils_group, text="Exit", command=close_gui).pack(fill='x', padx=4, pady=3)

# ========= MIDDLE: GRID + STATUS (grid inside center) =========
grid_frame = tk.Frame(center)
grid_frame.grid(row=0, column=0, sticky='nw') # anchor top-left, don't stretch vertically

for r in range(16):
    for c in range(16):
        idx = gui_to_strip_index(r, c)
        text = 'X' if idx == 135 else ''
        btn = tk.Button(grid_frame, width=1, height=1, bg="gray", text=text)
        btn.grid(row=r, column=c, padx=1, pady=1, sticky='nsew')
        btn.config(command=lambda i=idx, b=btn: toggle_led(i, b))
        led_buttons.append(btn)
        buttons_by_index[idx] = btn

# Status under the grid
status_group = ttk.LabelFrame(center, text='Status')
status_group.grid(row=1, column=0, sticky='nw', padx=0, pady=(2,0))
status_var = tk.StringVar(value='Idle')
status_label = tk.Label(status_group, textvariable=status_var, anchor='w', justify='left', wraplength=585)
status_label.pack(padx=8, pady=(4,2), anchor='w')
progress = ttk.Progressbar(status_group, mode='determinate', maximum=100, value=0, length=585)
progress.pack(padx=8, pady=(0,8), anchor='w')

# ========= RIGHT: MOTORS (pack inside right_motors) =========
# ----- STEP SIZE -----
step_group = ttk.LabelFrame(right_motors, text='Motor Control')
step_group.pack(fill='x', pady=(0,8))

row = tk.Frame(step_group); row.pack(fill='x', padx=4, pady=(6,4))
tk.Label(row, text='Step size (cycles):', width=18, anchor='w').pack(side='left')

selected_cycles_var = tk.IntVar(value=128)
step_combo = ttk.Combobox(row, state='readonly', width=8, values=('16','32','64','128','256','512'))
step_combo.set(str(selected_cycles_var.get()))
step_combo.pack(side='left')
step_combo.bind('<<ComboboxSelected>>', _on_step_combo)

# ----- Z FOCUS (Up/Down) -----
z_group = ttk.LabelFrame(right_motors, text='Z-axis Focus')
z_group.pack(fill='x', pady=(0,8))

# Optional: flip if wiring make Up/Down feel inverted
Z_UP_IS_FWD = False # set True/False to swap

zr = tk.Frame(z_group); zr.pack(fill='x', padx=6, pady=6)
def _z_up():
    _move_sel(MOTOR1_PINS, SEQ_HALF_FWD if Z_UP_IS_FWD else SEQ_HALF_BWD)
def _z_down():
    _move_sel(MOTOR1_PINS, SEQ_HALF_BWD if Z_UP_IS_FWD else SEQ_HALF_FWD)

tk.Button(zr, text='↑', width=10, command=_z_up).pack(side='left', padx=4)
tk.Button(zr, text='↓', width=10, command=_z_down).pack(side='left', padx=4)

# ----- Stage X+Y Translation -----
compass_group = ttk.LabelFrame(right_motors, text='Stage X + Y translation')
compass_group.pack(fill='x', pady=(6,8))

cg = tk.Frame(compass_group)
cg.pack(padx=6, pady=6)

# Due to the original OpenFlexure design, translation motors are at 45* so, true Up/Down/Left/Right drives X+Y motors together
def _go_north():
    # X forward + Y backward
    _move_two_sel(MOTOR2_PINS, SEQ_HALF_FWD, MOTOR3_PINS, SEQ_HALF_FWD)

def _go_south():
    # X backward + Y forward
    _move_two_sel(MOTOR2_PINS, SEQ_HALF_BWD, MOTOR3_PINS, SEQ_HALF_BWD)

def _go_east():
    # X forward + Y forward
    _move_two_sel(MOTOR2_PINS, SEQ_HALF_FWD, MOTOR3_PINS, SEQ_HALF_BWD)

def _go_west():
    # X backward + Y backward
    _move_two_sel(MOTOR2_PINS, SEQ_HALF_BWD, MOTOR3_PINS, SEQ_HALF_FWD)

# Layout
btnN = tk.Button(cg, text='↑', width=6, command=_go_north)
btnW = tk.Button(cg, text='←', width=6, command=_go_west)
btnE = tk.Button(cg, text='→', width=6, command=_go_east)
btnS = tk.Button(cg, text='↓', width=6, command=_go_south)

btnN.grid(row=0, column=1, padx=4, pady=2)
btnW.grid(row=1, column=0, padx=4, pady=2)
btnE.grid(row=1, column=2, padx=4, pady=2)
btnS.grid(row=2, column=1, padx=4, pady=2)

################################################
# Run GUI
################################################
root.mainloop()
