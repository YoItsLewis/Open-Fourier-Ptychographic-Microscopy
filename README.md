# Open Fourier Ptychographic Microscopy (OpenFPM)
## Background
Here we present a low-cost 3D printed multi-modal super-resolution microscope based on Fourier Ptychography. The original and modified 3D printed components from the Open Flexure Microscope (v7 high-resolution motorised microscope) framework. Additionally, we have constructed a canopy framework, which can easily be integrated to accompany existing Open FLexure Microscopy. This canopy consists of a number of 3D printed components which can be found in: blah blah. This canopy allows a new platform for illumination, which can be adjusted in height (optical (z-axis)) to the sample, and easily aligned in (x and y-axes), a critical step for any FPM algorithm. 

Additionally, we have adapted our own hardware configurations with a ready-to-go graphical user interface (via Python), using a Raspberry Pi model 4 B to correctly illuminate the LEDs (BTF-LIGHTING WS2812B RGB Individually Addressable Digital 16x16 array) and synchronise the image acquisition through hardware triggering the camera (iDS UI-3060CP Rev. 2.). The GUI is also capable of controlling the stepper-motors, used to move the sample in the x and y-axes, as well as focus the sample in the optical z-axis. Conventionally Adafruit LED array's have been used in FPM, these LEDs produce poor brightness levels in comparison to our LEDs. Therefore, this allows the camera sensor to collect signals from higher illumination angles, and from larger distances, which in turn allows the reconstruction algorithm to output a higher synthetic numerical (NA). 

It is important to note that for good FPM image outputs the reconstruction algorithm requires at least 9 brightfield images for the LED correction.

We have attempted to make this microscope as asseccable as possible using low-cost components and open source software scripts to construct a compact and portable super-resolution system.

## Image Modalities
Image modalities of this system include:
- BRIGHTFIELD
- DARKFIELD
- SUPER-RESOLUTION AMPLITUDE (FPM)
- SUPER-RESOLUTION PHASE (FPM)
- RHIENBERG CONTRAST (contrast enhancement)

It is also possible to capture RGB images using the 3-channels within each LED.

## Software
As we look to continue to make FPM more open-source and user-friendly, here is an outline of the pipeline used for obtained FPM images:
- Illumination, sample placement, z-focus: Python
- Reconstruction algorithm: MATLAB (open-source user friendly code)
- Post-processing: FIJI (FIJI is just ImageJ)

All software used to control the system can be found [here (hyperlink to GitHub folder with .stl files)].

## Optical components
The system uses a non-infinity corrected 10x/0.25 Comar objective, conventionally demonstrating a resolution of 1.27um (lambda = 363 nm) over a 1.33 mm diagonal field of view (FoV). However, by illuminating the sample at various angles using an array of LEDs and reconstructing using the Quasi-Newton Phase Retrieval algorithm for FPM, we are able to produce a sub-micron resolution ouput of 315 nm over a 1.22 mm diagonal FoV, allowing subcellular detail of many biological structures.
Non-infinity objective lens
- https://www.comaroptics.com/components/lenses/mounted-lenses/microscope-objectives (Comar Optics)
- https://www.edmundoptics.co.uk/c/finite-conjugate-objectives/708/ (Edmund Optics)

  We would suggest either of the following should be appropriate:   
  - https://www.edmundoptics.co.uk/f/commercial-grade-standard-microscope-objectives/12253/
  - https://www.edmundoptics.co.uk/f/international-standard-microscope-objectives/11958/   


## Citing

## Build Your Own 3D Printed FPM System
<p align='center'>
<img width='400' src='Images/FPM_Microscope_Image.png'>
</p>
Printed Parts
All 3D-printable files can be found [here (hyperlink to GitHub folder with .stl files)]. All files were printed in PLA Basic/Matte (whatever your preference is...), with 0.2 layer height, no supports needed.


## Assembly Instructions
Assembly instructions for the system can be found [here (hyperlink to GitHub folder with .stl files)].
