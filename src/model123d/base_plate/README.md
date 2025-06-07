# Base Plate for Miniatures

Prusa-ID: 1314888
Prusa-URL:

# Description
Base Plate for Miniatures

## Usage

### Separate Base (glue on)

- Decide if you want a "hexagonal" or "circular" 
- Measure your base and modify P.size in mm
- Define your thickness by modifying P.thickness in mm
- Define the magnet size via P.magnet_diameter and P.magnet_height in mm
  OR remove it complely by setting P.do_magnet = no 
- Generate the model P.do_export=yes will generate the STL file  
- Add it to your slicer, setup, print and glue it to your miniature
 

### Integrated Base (to a model of your liking)

- Open a miniature model in your slicer
- Decide if you want a "hexagonal" or "circular" 
- Measure your base and modify P.size  in mm
- Define your thickness by modifying P.thickness in mm
- Define the magnet size via P.magnet_diameter and P.magnet_height in mm
  OR remove it by setting P.do_magnet = no 
- Generate the model P.do_export=yes will generate the STL file  
- Add it to the miniature model, adapt the position to your liking.
- Slice, print and post your make


## Model Details

- Default settings for PETG
- Optional auto generated supports for the magnet
- around 10min print time for a base with 42 mm
- <6g of material with 42mm base



## Model Design

- Using build123d  a Python based OCCT library
- Exports STL as default.
 

## Notes

- Allowed use for commercial use 
- Send us the measurements if you need modified STL files or other output formats.


 