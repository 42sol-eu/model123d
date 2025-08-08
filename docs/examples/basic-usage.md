# Basic Usage Examples

Learn the fundamentals of creating and customizing 3D models with Model123d through practical examples.

## Example 1: Simple Box

Let's start with the most basic 3D shape - a parametric box.

```python
"""Simple parametric box example"""

from build123d import *
from build123d import MM as mm
from ocp_vscode import show
from dataclasses import dataclass

@dataclass
class P:
    """Parameters for our box"""
    width: float = 20.0 * mm
    height: float = 15.0 * mm  
    depth: float = 10.0 * mm
    do_fillet: bool = True
    fillet_radius: float = 2.0 * mm

# Create the box
with BuildPart() as box:
    Box(P.width, P.height, P.depth)
    
    if P.do_fillet:
        fillet(box.edges(), radius=P.fillet_radius)

# Visualize in VS Code
show(box)

# Export to STL
if True:  # Set to False to skip export
    exporter = Mesher()
    exporter.add_shape(box.part)
    exporter.write("simple_box.stl")
```

**Key Concepts:**
- ✅ Parameters defined in a dataclass
- ✅ Using build123d's declarative syntax
- ✅ Conditional features (`do_fillet`)
- ✅ Visualization with `show()`
- ✅ STL export

## Example 2: Cylinder with Holes

A more complex example showing how to subtract geometry.

```python
"""Cylinder with holes - demonstrates subtraction"""

from build123d import *
from build123d import MM as mm
from ocp_vscode import show
from dataclasses import dataclass

@dataclass  
class P:
    """Parameters for cylinder with holes"""
    cylinder_radius: float = 15.0 * mm
    cylinder_height: float = 20.0 * mm
    hole_radius: float = 3.0 * mm
    hole_count: int = 6
    hole_circle_radius: float = 10.0 * mm

# Create the cylinder
with BuildPart() as cylinder:
    # Main body
    Cylinder(radius=P.cylinder_radius, height=P.cylinder_height)
    
    # Create holes around the circumference
    with Locations(*[
        Location((
            P.hole_circle_radius * cos(i * 360° / P.hole_count),
            P.hole_circle_radius * sin(i * 360° / P.hole_count), 
            0
        )) for i in range(P.hole_count)
    ]):
        Cylinder(radius=P.hole_radius, height=P.cylinder_height, mode=Mode.SUBTRACT)

show(cylinder)
```

**Advanced Concepts:**
- ✅ Mathematical positioning with `cos()` and `sin()`
- ✅ List comprehensions for multiple locations
- ✅ Subtraction with `Mode.SUBTRACT`
- ✅ Complex parameter relationships

## Example 3: Custom Profile Extrusion

Creating complex shapes by extruding custom 2D profiles.

```python
"""Custom profile extrusion"""

from build123d import *
from build123d import MM as mm
from ocp_vscode import show
from dataclasses import dataclass

@dataclass
class P:
    """Parameters for extruded profile"""
    profile_width: float = 30.0 * mm
    profile_height: float = 15.0 * mm
    wall_thickness: float = 2.0 * mm
    extrude_length: float = 50.0 * mm
    corner_radius: float = 3.0 * mm

# Create custom 2D profile
with BuildPart() as profile:
    with BuildSketch() as sketch:
        # Outer rectangle
        RectangleRounded(
            P.profile_width, 
            P.profile_height, 
            radius=P.corner_radius
        )
        
        # Inner rectangle (creates wall thickness)
        RectangleRounded(
            P.profile_width - 2*P.wall_thickness,
            P.profile_height - 2*P.wall_thickness, 
            radius=P.corner_radius/2,
            mode=Mode.SUBTRACT
        )
    
    # Extrude the profile
    extrude(amount=P.extrude_length)

show(profile)
```

**Profile Concepts:**
- ✅ 2D sketching with `BuildSketch()`
- ✅ Rounded rectangles
- ✅ Creating hollow sections
- ✅ Extrusion operations

## Example 4: Assembly with Multiple Parts

Building complex models from multiple components.

```python
"""Multi-part assembly example"""

from build123d import *
from build123d import MM as mm
from ocp_vscode import show
from dataclasses import dataclass

@dataclass
class P:
    """Assembly parameters"""
    base_width: float = 40.0 * mm
    base_height: float = 8.0 * mm
    post_radius: float = 4.0 * mm
    post_height: float = 25.0 * mm
    top_radius: float = 8.0 * mm
    top_height: float = 5.0 * mm

# Create the base
with BuildPart() as base:
    Cylinder(radius=P.base_width/2, height=P.base_height)
    fillet(base.faces().sort_by(Axis.Z)[-1].edges(), radius=2.0)

# Create the post
with BuildPart() as post:
    Cylinder(radius=P.post_radius, height=P.post_height)

# Create the top
with BuildPart() as top:
    Cylinder(radius=P.top_radius, height=P.top_height)

# Assemble the parts
with BuildPart() as assembly:
    # Add base at origin
    add(base.part)
    
    # Add post on top of base
    add(post.part.moved(Location((0, 0, P.base_height))))
    
    # Add top on top of post  
    add(top.part.moved(Location((0, 0, P.base_height + P.post_height))))

# Color the parts for visualization
base.color = "#FF0000"      # Red base
post.color = "#00FF00"      # Green post  
top.color = "#0000FF"       # Blue top

show({
    "base": base,
    "post": post, 
    "top": top,
    "assembly": assembly
})
```

**Assembly Concepts:**
- ✅ Multiple `BuildPart()` contexts
- ✅ Part positioning with `Location()`
- ✅ Color assignment for visualization
- ✅ Organized display with dictionaries

## Example 5: Parametric Text

Adding text features to your models.

```python
"""Text feature example"""

from build123d import *
from build123d import MM as mm
from ocp_vscode import show
from dataclasses import dataclass

@dataclass
class P:
    """Text feature parameters"""
    base_width: float = 60.0 * mm
    base_height: float = 40.0 * mm
    base_depth: float = 5.0 * mm
    text_content: str = "Model123d"
    text_size: float = 8.0 * mm
    text_depth: float = 1.0 * mm
    font_style: FontStyle = FontStyle.BOLD

# Create base plate
with BuildPart() as base_plate:
    Box(P.base_width, P.base_height, P.base_depth)
    
    # Add text on top surface
    with BuildSketch(Plane.XY.offset(P.base_depth)) as text_sketch:
        Text(
            txt=P.text_content,
            font_size=P.text_size, 
            font_style=P.font_style
        )
    
    # Extrude text upward
    extrude(amount=P.text_depth, mode=Mode.ADD)
    
    # Optional: Emboss text instead of raising it
    # extrude(amount=-P.text_depth, mode=Mode.SUBTRACT)

show(base_plate)
```

**Text Concepts:**
- ✅ Text geometry creation
- ✅ Font styling options
- ✅ Raised vs embossed text
- ✅ Working with text planes

## Example 6: Pattern Arrays

Creating repeating patterns efficiently.

```python
"""Pattern array example"""

from build123d import *
from build123d import MM as mm
from ocp_vscode import show
from dataclasses import dataclass

@dataclass
class P:
    """Pattern parameters"""
    base_size: float = 50.0 * mm
    base_thickness: float = 3.0 * mm
    hole_diameter: float = 4.0 * mm
    hole_spacing: float = 8.0 * mm
    pattern_size: int = 5  # 5x5 grid

# Create base with hole pattern
with BuildPart() as patterned_base:
    # Create solid base
    Box(P.base_size, P.base_size, P.base_thickness)
    
    # Create hole pattern
    start_pos = -P.base_size/2 + P.hole_spacing
    positions = []
    
    for i in range(P.pattern_size):
        for j in range(P.pattern_size):
            x = start_pos + i * P.hole_spacing
            y = start_pos + j * P.hole_spacing
            positions.append(Location((x, y, 0)))
    
    # Create holes at all positions
    with Locations(*positions):
        Cylinder(
            radius=P.hole_diameter/2, 
            height=P.base_thickness,
            mode=Mode.SUBTRACT
        )

show(patterned_base)
```

**Pattern Concepts:**
- ✅ Nested loops for 2D patterns
- ✅ Calculated positioning
- ✅ Efficient hole creation
- ✅ Mathematical spacing

## Common Patterns

### Parameter Validation

Add validation to prevent invalid parameter combinations:

```python
@dataclass
class P:
    thickness: float = 3.0 * mm
    hole_diameter: float = 2.0 * mm
    
    def __post_init__(self):
        """Validate parameters after initialization"""
        if self.hole_diameter >= self.thickness:
            raise ValueError("Hole diameter must be less than thickness")
        if self.thickness <= 0:
            raise ValueError("Thickness must be positive")
```

### Debug Information

Add helpful debug output:

```python
def debug_info(obj, name="Object"):
    """Print useful information about a build123d object"""
    if hasattr(obj, 'part'):
        part = obj.part
        bb = part.bounding_box()
        print(f"{name}:")
        print(f"  Bounding box: {bb.size}")
        print(f"  Volume: {part.volume:.2f}")
        print(f"  Surface area: {part.surface_area():.2f}")
```

### File Management

Organize your exports:

```python
from pathlib import Path
from datetime import datetime

def export_with_timestamp(part, base_name):
    """Export with timestamp to avoid overwriting"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{base_name}_{timestamp}.stl"
    
    output_dir = Path("_output") 
    output_dir.mkdir(exist_ok=True)
    
    exporter = Mesher()
    exporter.add_shape(part)
    exporter.write(output_dir / filename)
    
    print(f"Exported: {filename}")
```

## Next Steps

Ready for more advanced techniques? Check out:

- **[Advanced Customization](advanced.md)** - Complex parametric relationships
- **[VS Code Integration](vscode.md)** - Maximize your development environment
- **[Model Development](../development/contributing.md)** - Create your own models

---

*Start with these examples and build your way up to complex parametric models! 🚀*
