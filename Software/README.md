# Software

### FPM GUI for controlling the illumination and translation
- 16x16 WS2812B LEDs
  - Colour
  - Brightness
  - 16x16 LED grid layout
- Timing
  - Exposure time (ms) - LED on
  - Capture time (ms) - LED off
- Patterns (User can make custom LED patterned in the code)
  - Hold - Brightfield (BF) and Darkfield (DF)
  - Triggered - Central 9 LEDs (3 LED diameter circle), 69  LEDs (9 LED diameter circle), 177 LEDs (15 LED diameter circle)
- Motor Control
  - Z-axis focus
  - Stage X and Y translation

<p align='center'>
<img width='800' src='.../Images/GUI.png'>
</p>

### Acquiring a live FFT from a screen region.
OpenFPM is designed with a translation LED array to allow the user to manually align the LED array into the optical axis for better reconstruction outputs. Alignment of the LED array is carried out by using a high contrast sample, and live observation of the brightfield coherent passbands in Fourier Space. This is supported using live on-screen FFT imaging of the sample using the FIJI macro linked below, with credit to the author, Nicolás De Francesco, user: @NicoDF.

Example images in image and Fourier space.

https://forum.image.sc/t/is-live-fft-of-an-roi-on-screen-possible/31026/4 (November 2019) [Accessed: March 2026]