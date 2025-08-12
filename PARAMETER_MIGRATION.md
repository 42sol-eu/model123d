# Parameter System Migration Plan

This document outlines the migration of the parameter system from model123d to noah123d for better reusability across projects.

## Current Status

✅ **Task 1**: Created noah123d-compatible parameters module
✅ **Task 2**: Updated model123d to use improved parameter system with descriptions

## Files Created

### 1. `noah123d_parameters.py` (for noah123d package)
This file contains the enhanced parameter system designed to be added to the noah123d package:

- **BaseParameters**: Core parameter class with debug, export, and naming functionality
- **GeometricParameters**: Specialized class for geometric dimensions
- **MaterialParameters**: Specialized class for material properties
- **Factory functions**: Dynamic parameter class creation
- **Improved naming**: Cleaner file naming without `=` signs
- **Descriptions**: Parameter descriptions for better documentation

### 2. Updated `parameters.py` (current model123d implementation)
Enhanced the existing parameters with:
- Parameter descriptions
- Cleaner naming format (`l20_w6_h4` instead of `l=20.0_w=6.0_h=4.0`)
- Better export path handling
- Improved documentation

## Next Steps

### For noah123d package:
1. **Add to noah123d repository**:
   ```bash
   cd /path/to/noah123d
   cp noah123d_parameters.py noah123d/parameters.py
   ```

2. **Update noah123d/__init__.py**:
   ```python
   from .parameters import BaseParameters, GeometricParameters, MaterialParameters, short_field
   ```

3. **Add tests** for the parameter system

4. **Update noah123d documentation** to include parameter system usage

### For model123d package:
1. **Install noah123d** as a dependency:
   ```toml
   # In pyproject.toml
   [tool.poetry.dependencies]
   noah123d = {git = "https://github.com/42sol-eu/noah123d.git"}
   ```

2. **Update imports** in stampinup/parameters.py:
   ```python
   # Replace local implementation with:
   from noah123d.parameters import BaseParameters as Parameters, short_field
   from noah123d import mm, yes, no
   ```

3. **Simplify ClipParameters**:
   ```python
   @dataclass
   class ClipParameters(Parameters):
       length: float = short_field(20.0, "l", "Overall length of the clip")
       width_inner: float = short_field(6.0, "w", "Inner width of the clip")  
       height_inner: float = short_field(4.0, "h", "Inner height of the clip")
       thickness: float = short_field(5.0, "t", "Wall thickness")
       fillet_radius: float = short_field(0.4, "fr", "Fillet radius for edges")
   ```

## Benefits After Migration

1. **Consistency**: All build123d projects can use the same parameter system
2. **Reusability**: Common parameter patterns available across projects  
3. **Documentation**: Built-in parameter descriptions
4. **Maintainability**: Single source of truth for parameter functionality
5. **Extensibility**: Easy to add new parameter types and utilities

## Example Usage (After Migration)

```python
from noah123d.parameters import BaseParameters, GeometricParameters, short_field

@dataclass
class MyModelParameters(GeometricParameters):
    """Custom parameters for my model"""
    special_feature: bool = short_field(True, "sf", "Enable special feature")
    material_thickness: float = short_field(2.0, "mt", "Material thickness")
    
    def custom_validation(self):
        """Add custom validation logic"""
        if self.length < self.width:
            raise ValueError("Length must be >= width")

# Usage
params = MyModelParameters(length=30, width=20, special_feature=False)
print(params)  # Shows descriptions
filename = f"model{params.name()}.stl"  # Clean naming: model__l30_w20_h10_sf0_mt2.stl
```

## Testing

Both the current improved system and the noah123d-ready system have been tested and work correctly:
- ✅ Parameter creation and validation
- ✅ Compact naming generation  
- ✅ Export path generation
- ✅ String representation with descriptions
- ✅ Backward compatibility

The migration path preserves all existing functionality while adding new capabilities.
