# Open Fourier Ptychographic Microscopy (OpenFPM)
Open Fourier Ptychographic Microscopy (OpenFPM) is an open-source microscope platform for performing computational microscopy. Its fundamentally microscope body is based the [OpenFlexure Project](https://openflexure.org/projects/microscope/build) on version 7.

## Paper and Citation
Please consider citing our 2026 paper:


## Build Your Own OpenFPM system
<p align='center'>
<img width='800' src='Images/Figure 1.png'>
</p>

### Hardware

All 3D printed components were fabricated using a fused deposition modelling (FDM) printer with matte black polylactic acid (PLA) filament at 0.2 mm layer height. Default print setting were used and automatic tree supports were applied.

We found using the [Bambu Labs P1S 3D Printer](https://uk.store.bambulab.com/products/p1s?id=578772891943051270) to be reliable.

#### Material Costs 

Note. This billing list is based on starting from scratch, and you may already have items such as a 3D printer, M6 screws, a laptop, etc.

| Parts | Purpose | Source | Quantity | Price (£) |
|-----|-----|-----|-----|-----|
| **Electronic Components** |
| Raspberry Pi 4 Model B Starter Kit (8GB) | Microcomputer for controlling the microscope | [The Pi Hut](https://thepihut.com/products/raspberry-pi-starter-kit?variant=31994566639678) | 1 | ~£130 |
| Raspberry Pi Keyboard & Mouse | Primary input devices for interacting with the Raspberry Pi | [The Pi Hut](https://thepihut.com/products/official-raspberry-pi-keyboard-mouse?variant=18828277383230) | 1 | ~£24 |
| 28BYJ-48 5V Stepper Motor + Driver Board | Objective focus and X-Y sample translation | [Amazon](https://www.amazon.co.uk/GeeekPi-Stepper-28BYJ-48-Uln2003-Compatible/dp/B087BYKB6T/ref=sr_1_5?dib=eyJ2IjoiMSJ9.tpKbALur4RZR5JjIbrZBahg9M0IhaDgmiF7VwBWE_2lsTL00-iRC6xXIvnyfChnaYqPoV9Gr50YNRAiiWclIkc7meNSNdmMirNrMPg_gOMrreA9ZntPfVBQ38vUR9fwi93x8wK9a9-xv7wTnYonW1l5yaqqH8dDyoqPMSYfvQgSfoi7agcg3Q4DXaJho1xlHV60y0XfS1d2ZRnEMOHDfPPFEu1HbcgymNHAHrIat6Jai5Hy_woxu5Wi1DnVFxtKRGXrG9qPlf7OP2aix-48fc58KT13RH6gw9dvW76QfDPg._fRZJClR4FFzt0LQ7L6sIkDKB9mwDvTVIwPNkDp-gEc&dib_tag=se&keywords=28byj-48&qid=1773853029&sr=8-5) | 1 | ~£16 |
| WS2812B RGB 16x16 LED Array | Microscope illumination source | [Amazon](https://www.amazon.co.uk/BTF-LIGHTING-Individual-Addressable-Flexible-Controllers/dp/B088K1JH6X/ref=sr_1_4?crid=1TDCCR1PVHEZI&dib=eyJ2IjoiMSJ9.BlBbfjaxQD81QRlFc0RoykGyvNqepSEBWBUXSh5dhH8Izaq5I3eHLzQNwcP58zJ_g5KJcmAz3sXc5WHSyN3tFMFqY885Ji_6wpYi1NJLEjbaBzJerwrchq3Al4w8YoxB44xzRurl0KOIqh-5-MLe0q_TGN8MHpB84Jl03lWM88kHzF7ABw2D_dwZOi-cpTNZaxy0pDkv0YXhD4YJeiqqaFl3o17sfhu8GvuNenMw-57pwuYcKO2ADKH5zCnCxQtYtTxeWC3wZmMnI0opGIlZ_wdnl_BQJ4-rvEX3ecfqd6A.ILqKG4o1fKNMmcr2hGjSUMYwglu0uDxfSaB0AR59xHk&dib_tag=se&keywords=led%2Barray&qid=1773851490&s=kitchen&sprefix=led%2Barray%2Ckitchen%2C222&sr=1-4&th=1) | 1 | ~£20 |
| Breadboard and Jumper Wires Kit | Wiring for connecting the microcomputer to the LED array + Motors | [Amazon](https://www.amazon.co.uk/HUAREW-Breadboard-Jumper-Include-Points/dp/B0B5TCKTQH/ref=sr_1_4_sspa?crid=314GBN29Q2J8Q&dib=eyJ2IjoiMSJ9.Vdt6Ti1-DwLZVl5Jd0sx8KltvLq3nGuI3O04CljjMjJocwzI61z4BB8c2a6rk0_9YaFVxERGaFBxc0RotFdqHZlzmlmX0Bp-n_uB6315HeygDOw5QO-6VEgO0mXQDr6mDOv0xnvJ4iTOfin41Tiof4i14ME5M7KTHz8C8Um_5GoPDg4zJ0oTeF5nXYIctct5aNjJOGhbHd2HcHNLUlW4ldUbhzsSWMjL6NehSN-cv4WeTMtcGuIXSskGMmhh-G8XeVrsZpbGsGJ7sSK_u00s51z4WUAfj5VZ1297tedRsZ0.nCFNU3pLaWR8MUiCFS34yDLuV5LY6le9KtSD54dFcJU&dib_tag=se&keywords=electronics+breadboard&qid=1773851170&sprefix=electronics+breadboard%2Caps%2C253&sr=8-4-spons&aref=b7CJuJoBlm&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1) | 1 | ~£13 |
| Monochromatic Camera (c-mount) | Acquiring image data | [Edmund Optics](https://www.edmundoptics.co.uk/c/cameras/1012/#27915=27915_s%3AC-Mount&397021=397021_s%3AMonochrome&29401=29401_s%3AIDS) | 1 | ~£300 (Based on iDS camera. Price varies!) |
| USB 3.0 A to Right-Angle Micro B Cable | Provides power to the camera and transfers image data | [Thorlabs](https://www.thorlabs.com/item/CABU32) | 1 | ~£17 |
| 8 Pin Hirose Camera Cable | Cable for triggering camera from microcomputer | [Amazon](https://www.amazon.co.uk/Alvins-Cables-HR25-7TP-8S-Imaging-Industrial/dp/B08FD6B262?source=ps-sl-shoppingads-lpcontext&ref_=fplfs&th=1) | 1 | ~£25 |
| **Total** |||| ~ £545 |
| **Optomechanical Components** |
| Finite Conjugate Objective Lens | Objective lens for microscope | [Edmund Optics](https://www.edmundoptics.com/f/commercial-grade-standard-microscope-objectives/12253/) | 1 | ~£152 |
| ⌀1" Protected Aluminum Mirror | To redirect the light path into the camera | [Thorlabs](https://www.thorlabs.com/item/PF10-03-G01) | 1 | ~£50 |
| M6 Cap Screw and Hardware Kit | Screws, washers and nuts | [Thorlabs](https://www.thorlabs.com/item/HW-KIT2_M) | 1 | ~£120 |
| **Total** |||| ~£322 |
| **Equipment and Tools** |
| 10 Piece T Metric Hex Key Set | For tightening screws | [RS UK](https://uk.rs-online.com/web/p/hex-keys/0537811?cm_mmc=UK-PLA-DS3A-_-google-_-CSS_UK_EN_PMAX_RS+PRO+Focus-_--_-537811&matchtype=&&gclsrc=aw.ds&gad_source=1&gad_campaignid=22574727794&gbraid=0AAAAADkeWNMg7XDZ_q49dnlo4-gfSXvsK&gclid=Cj0KCQjwmunNBhDbARIsAOndKpkcEzOdYbLkLIusOwGEGe8-EovpMyIJTA_JNukP1wvmx2jJwT21N_UaAhkqEALw_wcB) | 1 | ~£34 |
| Bambu Labs P1S 3D Printer | Printing the microscope components | [Bambu Labs](https://uk.store.bambulab.com/products/p1s?id=578772891943051270) | 1 | ~£600 (Usually discounted!) |
| PC Monitor| Monitor Screen for Raspberry Pi | [Currys](https://www.currys.co.uk/computing/computer-monitors/pc-monitors) | 1 | ~£60 |
| Laptop | External laptop/PC for image reconstruction and processing | [Currys](https://www.currys.co.uk/products/hp-omnibook-7-ngai-17.3-laptop-intel-core-ultra-7-1-tb-ssd-32gb-ram-silver-10282690.html) | 1 | ~£1600 (A decent spec laptop) |
| **Total** |||| ~£2294 |
| **Overall Total** |||| ~£3161 |

## Assembly Instructions

Instructions for building an OpenFPM system can be found [here](https://github.com/YoItsLewis/Open-Fourier-Ptychographic-Microscopy/tree/main/Assembly%20Instructions).

## Software

[Link](https://core-electronics.com.au/guides/fully-addressable-rgb-raspberry-pi/) to set up the NeoPixel library on the Raspberry Pi for controlling the WS2812B RGB LEDs.

Python script for controlling the microscope 

## Datasets

Due to file size constraints, raw datasets for the Siemen star (Red illumination) and Blood smear (RGB 3-channel illumination) using OpenFPM are hosted externally in the [Strathclyde Data Repository](https://pureportal.strath.ac.uk/en/persons/lewis-walker-2/).