# 3D Printing Files

This directory contains the complete set of 3D design files for the OpenFPM microscope components. The files are provided in multiple formats to support a range of workflows, from direct 3D printing to further design modification and customisation.

### Folder Structure

The files are organised into three subfolder:

- F3D/
 - Native Autodesk Fusion 360 design files.
 - These are fully parametric and intended for users who wish to modify or adapt the designs.

- STEP/
 - Standard CAD exchange files (.step).
 - Suitable for use in a wide range of CAD software for inspection, modification, or integration into other assemblies.

- STL/
 - Mesh files for direct 3D printing.
 - These are ready to slice and can be used with most 3D printing software. (e.g. Bambu Studio, LycheeSlicer).

### Usage 

- For direct printing, use the files in the STL/ folder.
- For design modification or customisation, use the F3D/ or STEP/ files depending on your preferred CAD software.

### Notes

- All  components are designed to be compatible with the OpenFPM system architecture.
- Print settings (e.g. material, infill, layer height) may be adjusted depending on your printer and desired mechanical performance.
- Some parts may require support structures depending on orientation, this can usually be auto-checked in slice software.