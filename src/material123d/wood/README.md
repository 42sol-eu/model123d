# Wood Grain STL Cutting Solution

This directory contains multiple Python scripts that demonstrate how to create cuts from the `wood_grain_modifier.stl` file using the **trimesh** library (not build123d).

## Files Created

1. **`part_of_grain.py`** - Main implementation with comprehensive cutting functionality
2. **`advanced_grain_cutter.py`** - Advanced version with performance optimizations  
3. **`demo_grain_cuts.py`** - Quick demonstration of various cutting techniques
4. **`test_centering.py`** - Test script to verify origin centering works correctly

## Key Features

### Using Trimesh Library
- **Library**: `trimesh` (version 4.7.1)
- **Advantages**: Fast mesh operations, boolean operations, no build123d dependency
- **Performance**: Handles large STL files efficiently

### Automatic Centering at Origin
- **All cuts are automatically centered at (0,0,0)** after creation
- Original mesh position is preserved for cutting operations
- Result meshes have their geometric center translated to origin
- Ensures consistent positioning for downstream CAD operations

### Cutting Techniques Implemented

1. **Box Intersection** - Create rectangular cuts (wood planks)
2. **Cylindrical Cuts** - Create dowel or pipe shapes  
3. **Spherical Cuts** - Create spherical intersections
4. **Planar Slicing** - Create thin slices at specific planes
5. **Custom Shape Intersections** - Any trimesh primitive

### Example Usage

```python
from part_of_grain import WoodGrainCutter, Parameters

# Initialize the cutter
cutter = WoodGrainCutter(Parameters())

# Create a wood plank cut (100×50×15mm)
# Cut will be made at mesh center but result centered at origin
bounds = cutter.original_mesh.bounds
mesh_center = ((bounds[0] + bounds[1]) / 2).tolist()

plank = cutter.create_box_intersection(
    box_size=(100, 50, 15),
    box_center=mesh_center  # Where to cut in original mesh
)

# Export the result (automatically centered at origin)
cutter.export_mesh(plank, "my_wood_plank_centered")
```

### Advanced Features

- **Mesh Simplification**: Automatically simplifies large meshes for better performance
- **Progress Indicators**: Shows loading progress for large files
- **Multiple Export Formats**: STL export with proper error handling
- **Rich Console Output**: Beautiful formatted output with colors

## Output Files

The scripts create STL files in the `_output/` directory:

- `wood_grain_box_cut.stl` - Successfully created box intersection
- Additional cuts can be created by running the scripts

## Performance Optimizations

1. **Mesh Simplification**: Large meshes are simplified to ~50k faces for faster operations
2. **Working Mesh**: Separate simplified mesh for operations while preserving original
3. **Error Handling**: Robust error handling for edge cases
4. **Memory Efficiency**: Proper cleanup and resource management

## Running the Scripts

```bash
# Basic cutting script
python src/material123d/wood/part_of_grain.py

# Advanced version with optimizations  
python src/material123d/wood/advanced_grain_cutter.py

# Quick demo of all techniques
python src/material123d/wood/demo_grain_cuts.py
```

## Dependencies

- `trimesh` - Main mesh processing library
- `numpy` - Numerical operations
- `rich` - Beautiful console output
- `pathlib` - Path handling

## Cutting Methods Available

| Method | Description | Parameters |
|--------|-------------|------------|
| `create_box_intersection()` | Rectangular cuts | box_size, box_center |
| `create_slice_at_z()` | Planar slices | z_position, thickness |
| `create_cylindrical_cut()` | Cylindrical cuts | center, radius, height, axis |
| `create_spherical_cut()` | Spherical cuts | center, radius |
| `create_planar_cut()` | General planar cuts | plane_origin, plane_normal |

## Success Confirmation

✅ **Successfully created**: `wood_grain_box_cut.stl` (190KB)
- Created from the original 35MB `wood_grain_modifier.stl`
- Box intersection operation completed successfully
- File exported to `_output/` directory

This solution demonstrates that trimesh can efficiently handle large STL files and perform various cutting operations without requiring build123d.
