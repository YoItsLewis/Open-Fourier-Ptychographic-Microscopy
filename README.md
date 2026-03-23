# Open Fourier Ptychographic Microscopy (OpenFPM)
**Open Fourier Ptychographic Microscopy (OpenFPM)** is a low-cost, modular, and open-source platform for Fourier Ptychographic Microscopy (FPM). It combines programmable LED illumination, 3D-printed optomechanical components, and computational reconstruction to enable high-resolution, wide field-of-view imaging using accessible hardware. The microscope body is fundamentally based on version 7 of the [OpenFlexure Project](https://openflexure.org/projects/microscope/build).

Traditional FPM systems are often built by modifying commercial microscopes or through bespoke custom-built setups, both of which can limit flexibility, accessibility, and reproducibility. OpenFPM addresses this by providing a fully integrated, purpose-built architecture in which optics, illumination, mechanics, and control software are designed to work together seamlessly.

The platform supports multi-angle illumination, synthetic numerical aperture enhancement, and digital aberration correction, while remaining compact and affordable. By leveraging open-source design files and widely available components, OpenFPM lowers the barrier to entry for computational microscopy in research, education, and resource-limited environments.

## Paper and Citation
Our 2026 bioRxiv preprint is now available:

Walker, Lewis D., et al. "Open Fourier Ptychographic Microscopy (OpenFPM)." bioRxiv (2026): 2026-03.

Please consider citing out  2026 paper:

TBC...

## Build Your Own OpenFPM system
<p align='center'>
<img width='800' src='Images/Figure 1.png'>
</p>

### Hardware

All 3D-printed components were fabricated using a fused deposition modelling (FDM) printer with matte black polylactic acid (PLA) filament at a 0.2 mm layer height. Default print settings were used, and automatic tree supports were applied where necessary.

We found the [Bambu Labs P1S 3D Printer](https://uk.store.bambulab.com/products/p1s?id=578772891943051270) to be reliable.

#### Material Costs

Materials list for building an OpenFPM system, assuming users have access to IT equipment and tools for printing and optomechanics.

| Parts | Purpose | Source | Quantity | Price (£) |
|-----|-----|-----|-----|-----|
| **Electronic Components** |
| Raspberry Pi 4 Model B Starter Kit (1GB) | Microcomputer for controlling the microscope | [The Pi Hut](https://thepihut.com/products/raspberry-pi-starter-kit?srsltid=AfmBOoqbFpfRUvJug9U0IUKZXNz2ZsnnAsgzD-O2ssctK8kTpJ7MEXZv&variant=41173475754179) | 1 | ~£57 |
| 28BYJ-48 5V Stepper Motor + Driver Board | Objective focus and X-Y sample translation | [Amazon](https://www.amazon.co.uk/GeeekPi-Stepper-28BYJ-48-Uln2003-Compatible/dp/B087BYKB6T/ref=sr_1_5?dib=eyJ2IjoiMSJ9.tpKbALur4RZR5JjIbrZBahg9M0IhaDgmiF7VwBWE_2lsTL00-iRC6xXIvnyfChnaYqPoV9Gr50YNRAiiWclIkc7meNSNdmMirNrMPg_gOMrreA9ZntPfVBQ38vUR9fwi93x8wK9a9-xv7wTnYonW1l5yaqqH8dDyoqPMSYfvQgSfoi7agcg3Q4DXaJho1xlHV60y0XfS1d2ZRnEMOHDfPPFEu1HbcgymNHAHrIat6Jai5Hy_woxu5Wi1DnVFxtKRGXrG9qPlf7OP2aix-48fc58KT13RH6gw9dvW76QfDPg._fRZJClR4FFzt0LQ7L6sIkDKB9mwDvTVIwPNkDp-gEc&dib_tag=se&keywords=28byj-48&qid=1773853029&sr=8-5) | 1 | ~£16 |
| WS2812B RGB 16x16 LED Array | Microscope illumination source | [Amazon](https://www.amazon.co.uk/BTF-LIGHTING-Individual-Addressable-Flexible-Controllers/dp/B088K1JH6X/ref=sr_1_4?crid=1TDCCR1PVHEZI&dib=eyJ2IjoiMSJ9.BlBbfjaxQD81QRlFc0RoykGyvNqepSEBWBUXSh5dhH8Izaq5I3eHLzQNwcP58zJ_g5KJcmAz3sXc5WHSyN3tFMFqY885Ji_6wpYi1NJLEjbaBzJerwrchq3Al4w8YoxB44xzRurl0KOIqh-5-MLe0q_TGN8MHpB84Jl03lWM88kHzF7ABw2D_dwZOi-cpTNZaxy0pDkv0YXhD4YJeiqqaFl3o17sfhu8GvuNenMw-57pwuYcKO2ADKH5zCnCxQtYtTxeWC3wZmMnI0opGIlZ_wdnl_BQJ4-rvEX3ecfqd6A.ILqKG4o1fKNMmcr2hGjSUMYwglu0uDxfSaB0AR59xHk&dib_tag=se&keywords=led%2Barray&qid=1773851490&s=kitchen&sprefix=led%2Barray%2Ckitchen%2C222&sr=1-4&th=1) | 1 | ~£20 |
| Breadboard and Jumper Wires Kit | Wiring for connecting the microcomputer to the LED array + Motors | [Amazon](https://www.amazon.co.uk/HUAREW-Breadboard-Jumper-Include-Points/dp/B0B5TCKTQH/ref=sr_1_4_sspa?crid=314GBN29Q2J8Q&dib=eyJ2IjoiMSJ9.Vdt6Ti1-DwLZVl5Jd0sx8KltvLq3nGuI3O04CljjMjJocwzI61z4BB8c2a6rk0_9YaFVxERGaFBxc0RotFdqHZlzmlmX0Bp-n_uB6315HeygDOw5QO-6VEgO0mXQDr6mDOv0xnvJ4iTOfin41Tiof4i14ME5M7KTHz8C8Um_5GoPDg4zJ0oTeF5nXYIctct5aNjJOGhbHd2HcHNLUlW4ldUbhzsSWMjL6NehSN-cv4WeTMtcGuIXSskGMmhh-G8XeVrsZpbGsGJ7sSK_u00s51z4WUAfj5VZ1297tedRsZ0.nCFNU3pLaWR8MUiCFS34yDLuV5LY6le9KtSD54dFcJU&dib_tag=se&keywords=electronics+breadboard&qid=1773851170&sprefix=electronics+breadboard%2Caps%2C253&sr=8-4-spons&aref=b7CJuJoBlm&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1) | 1 | ~£13 |
| Monochromatic Camera (c-mount) | Acquiring image data | [Edmund Optics](https://www.edmundoptics.co.uk/c/cameras/1012/#27915=27915_s%3AC-Mount&397021=397021_s%3AMonochrome&29401=29401_s%3AIDS) | 1 | ~£300 (Based on iDS camera) |
| USB 3.0 A to Right-Angle Micro B Cable | Provides power to the camera and transfers image data | [Thorlabs](https://www.thorlabs.com/item/CABU32) | 1 | ~£17 |
| 8 Pin Hirose Camera Cable | Cable for triggering camera from microcomputer | [Amazon](https://www.amazon.co.uk/Alvins-Cables-HR25-7TP-8S-Imaging-Industrial/dp/B08FD6B262?source=ps-sl-shoppingads-lpcontext&ref_=fplfs&th=1) | 1 | ~£25 |
| **Total** |||| ~ £448 |
| **Optomechanical Components** |
| Finite Conjugate Objective Lens | Objective lens for microscope | [Edmund Optics](https://www.edmundoptics.com/f/commercial-grade-standard-microscope-objectives/12253/) | 1 | ~£152 (10x/0.25 Plan) |
| ⌀1" Protected Aluminum Mirror | Redirect light path onto camera sensor | [Thorlabs](https://www.thorlabs.com/item/PF10-03-G01) | 1 | ~£50 |
| M6 x 16 mm | Screw for combining the LED box hat to the LED box holder | | 1 | |
| M6 x 20 mm | Screws, washers and nuts for combining external post to microscope base plate | | 3 | |
| M6 x 25 mm | Screws for pin and hole system | | 3 | |
| M6 x 30 mm | Screws and nuts for combining internal post to LED canopy | | 3 | |
| **Total** |||| ~£202 |
| **Overall Total** |||| ~£650 |

## Assembly Instructions

Instructions for building an OpenFPM system can be found [here](https://github.com/YoItsLewis/Open-Fourier-Ptychographic-Microscopy/tree/main/Assembly%20Instructions).

External instruction for assembling the microscope body can be found [here](https://build.openflexure.org/openflexure-microscope/v7.0.0-beta5/high_res_microscope.html). 

## Software

[Link](https://core-electronics.com.au/guides/fully-addressable-rgb-raspberry-pi/) to set up the NeoPixel library on the Raspberry Pi for controlling the WS2812B RGB LEDs.

[Script](https://github.com/YoItsLewis/Open-Fourier-Ptychographic-Microscopy/tree/main/Software) for controlling the microscope via the Raspberry Pi. The graphical user interface has been tested using both a monitor and through remote desktop connection.

## Datasets

Due to file size constraints, raw datasets for the Siemen star (Red illumination) and Blood smear (RGB 3-channel illumination) using OpenFPM are hosted externally in the [Strathclyde Data Repository](https://pureportal.strath.ac.uk/en/persons/lewis-walker-2/).