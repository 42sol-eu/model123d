# Quick Start

Get up and running with Model123d in just a few minutes! This guide will walk you through creating your first parametric 3D model.

## Your First Model

Let's start by creating a simple base plate for miniatures - one of the most popular models in the collection.

### Step 1: Navigate to the Model

```bash
cd src/model123d/base_plate/
```

### Step 2: Examine the Parameters

Open the base plate model file and look at the parameters:

```python
@dataclass
class P:
    """Parameters for the Base Plate model."""
    do_export: bool = True
    do_pattern: bool = False  
    do_magnet: bool = True
    size: float = 42.0 * mm
    thickness: float = 4.5 * mm
    magnet_diameter: float = 10.0 * mm
    magnet_height: float = 3.0 * mm
    type: str = "Hexagonal"  # "Hexagonal" or "Circular"
```

### Step 3: Customize Your Model

Edit the parameters to match your needs:

=== "Hexagonal Base"

    ```python
    @dataclass
    class P:
        do_export: bool = True
        do_magnet: bool = True
        size: float = 32.0 * mm      # Smaller base
        thickness: float = 2.5 * mm   # Thinner profile
        magnet_diameter: float = 8.0 * mm
        magnet_height: float = 2.0 * mm
        type: str = "Hexagonal"
    ```

=== "Circular Base"

    ```python
    @dataclass
    class P:
        do_export: bool = True
        do_magnet: bool = True
        size: float = 50.0 * mm      # Larger base
        thickness: float = 3.0 * mm
        magnet_diameter: float = 12.0 * mm
        magnet_height: float = 3.0 * mm
        type: str = "Circular"
    ```

=== "No Magnet"

    ```python
    @dataclass
    class P:
        do_export: bool = True
        do_magnet: bool = False      # Disable magnet hole
        size: float = 25.0 * mm      # Small base
        thickness: float = 1.5 * mm  # Very thin
        type: str = "Circular"
    ```

### Step 4: Generate the Model

Run the Python script to generate your model:

```bash
python base_plate_Hexagonal_42.0_4.5_10.0.py
```

!!! success "Output"
    You should see colorful terminal output showing the build process, and an STL file will be generated in the `_output` directory.

### Step 5: View Your Model

If you're using VS Code with the OCP CAD Viewer extension, you'll see a 3D preview of your model directly in the editor!

## Understanding the Output

When you run a model, several things happen:

1. **Parameters are processed** - The script reads your parameter values
2. **3D geometry is created** - Using build123d to construct the model  
3. **Visualization** - The model is displayed in VS Code (if available)
4. **Export** - STL file is written to disk (if `do_export = True`)

### File Naming Convention

Generated files follow this pattern:
```
base_plate_{type}_{size}_{thickness}_{magnet_diameter}.stl
```

For example:
- `base_plate_Hexagonal_32.0_2.5_8.0.stl`
- `base_plate_Circular_50.0_3.0_12.0.stl`

## Common Workflows

### Design Iteration

1. **Modify parameters** in the Python file
2. **Run the script** to generate a new STL
3. **Import into your slicer** to check the result
4. **Repeat** until satisfied

### Batch Generation

Create multiple variants by running with different parameters:

```bash
# Create a small, medium, and large base
python -c "
from base_plate_template import *
for size in [25.0, 32.0, 42.0]:
    P.size = size * mm
    P.do_export = True
    # ... rest of your model code
"
```

### Slicer Integration

1. **Export your STL** with `do_export = True`
2. **Import into your slicer** (PrusaSlicer, Cura, etc.)
3. **Configure print settings**:
   - Layer height: 0.1-0.2mm
   - Infill: 20%
   - Material: PETG recommended
4. **Print and enjoy!**

## Next Model: Belt-A Pouch

Ready for something more complex? Try the Belt-A phone pouch:

```bash
cd ../belta/
python cmf_phone_belta.py
```

This model demonstrates:
- **Complex geometry** with curves and cutouts
- **Multiple components** (case, top, accessories)
- **Advanced features** like MOLLE attachments

## VS Code Tips

!!! tip "Pro Tips for VS Code Users"
    
    **Live Preview**: Models update in real-time as you modify parameters
    
    **Debug Mode**: Set `P.show_debug = True` for detailed build information
    
    **Color Coding**: Different components are automatically colored for easy identification
    
    **Measurement Tools**: Use the viewer to measure distances and angles

## Troubleshooting

### Model Not Generating

Check that:
- ✅ You're in the correct directory
- ✅ Dependencies are installed (`uv sync`)
- ✅ `do_export = True` in parameters
- ✅ No syntax errors in the Python file

### STL File Issues

- **File too large**: Reduce complexity or size parameters
- **File too small**: Check your units (use `* mm` for millimeters)
- **Weird geometry**: Verify parameter values are reasonable

### VS Code Not Showing Model

- Install the OCP CAD Viewer extension
- Make sure `ocp-vscode` package is installed
- Try restarting VS Code

## What's Next?

Now that you've created your first model, explore:

- 📁 [Project Structure](project-structure.md) - Understand how models are organized
- 🎯 [All Models](../models/base-plates.md) - Browse the complete collection
- 🛠️ [Development Guide](../development/contributing.md) - Create your own models

Happy modeling! 🎉
