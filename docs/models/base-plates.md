# Base Plates for Miniatures

Professional-quality base plates for tabletop gaming miniatures with integrated magnet holes for magnetic storage systems.

!!! info "Printables"
    This model is available on Printables: [Base Plate for Miniatures #1314888](https://www.printables.com/model/1314888)

## Overview

The base plate system provides customizable foundations for miniature gaming figures. Whether you need hexagonal bases for wargaming or circular bases for RPGs, this parametric system has you covered.

### Key Features

- ✅ **Two base shapes**: Hexagonal and Circular
- ✅ **Integrated magnets**: Optional magnet holes for storage
- ✅ **Fully parametric**: Adjust size, thickness, and magnet specifications
- ✅ **Quick generation**: Generate STL files in seconds
- ✅ **Print-optimized**: Designed for easy 3D printing

## Usage Scenarios

### Separate Base (Glue-on)

Perfect for adding magnetic capabilities to existing miniatures:

1. **Choose your shape** - Hexagonal or Circular
2. **Measure your miniature's base** and set `P.size`
3. **Set thickness** via `P.thickness` 
4. **Configure magnet** with `P.magnet_diameter` and `P.magnet_height`
5. **Generate and print** the base
6. **Glue to your miniature**

### Integrated Base (Built-in)

For new miniature designs or when printing your own figures:

1. **Open your miniature model** in your slicer
2. **Generate the base plate** STL with your desired parameters
3. **Import the base** into your slicer alongside the miniature
4. **Position appropriately** and slice together
5. **Print as one piece**

## Parameters

### Basic Configuration

```python
@dataclass
class P:
    """Parameters for the Base Plate model."""
    do_export: bool = True           # Generate STL file
    do_pattern: bool = False         # Pattern mode (not implemented)
    do_magnet: bool = True          # Include magnet hole
    size: float = 42.0 * mm         # Base diameter/width
    thickness: float = 4.5 * mm     # Base thickness  
    magnet_diameter: float = 10.0 * mm  # Magnet hole diameter
    magnet_height: float = 3.0 * mm     # Magnet hole depth
    type: str = "Hexagonal"         # "Hexagonal" or "Circular"
```

### Parameter Details

| Parameter | Description | Typical Range | Notes |
|-----------|-------------|---------------|-------|
| `size` | Base diameter (circular) or width (hexagonal) | 20-60mm | Match your miniature's base |
| `thickness` | Base plate thickness | 1.5-6.0mm | Thicker = more durable |
| `magnet_diameter` | Magnet hole diameter | 6-15mm | Match your magnet size |
| `magnet_height` | Depth of magnet hole | 2-5mm | Should be ≤ thickness |
| `type` | Base shape | "Hexagonal" or "Circular" | Choose based on your game |

## Common Configurations

### Warhammer 40K (32mm Hexagonal)

```python
P.size = 32.0 * mm
P.thickness = 2.5 * mm
P.magnet_diameter = 8.0 * mm
P.magnet_height = 2.0 * mm
P.type = "Hexagonal"
```

### D&D Medium Creature (25mm Circular)

```python
P.size = 25.0 * mm  
P.thickness = 3.0 * mm
P.magnet_diameter = 6.0 * mm
P.magnet_height = 2.5 * mm
P.type = "Circular"
```

### Large Miniature (50mm Circular)

```python
P.size = 50.0 * mm
P.thickness = 4.0 * mm  
P.magnet_diameter = 12.0 * mm
P.magnet_height = 3.0 * mm
P.type = "Circular"
```

### No Magnet Version

```python
P.size = 32.0 * mm
P.thickness = 1.5 * mm
P.do_magnet = False  # Disable magnet hole
P.type = "Hexagonal"
```

## Generated Files

The model generates STL files with descriptive names:

```
base_plate_{type}_{size}_{thickness}_{magnet_diameter}.stl
```

**Examples:**
- `base_plate_Hexagonal_32.0_2.5_8.0.stl`
- `base_plate_Circular_25.0_3.0_6.0.stl`
- `base_plate_Hexagonal_42.0_4.5_10.0.stl`

## Print Settings

### Recommended Settings

| Setting | Value | Notes |
|---------|-------|-------|
| **Material** | PETG (preferred), PLA, ABS | PETG is most durable |
| **Layer Height** | 0.1-0.2mm | 0.1mm for finest detail |
| **Infill** | 20-30% | Higher for durability |
| **Perimeters** | 3-4 | Ensures strength |
| **Support** | Auto (for magnet holes) | Only if magnet is deep |

### Print Time & Material

| Base Size | Layer Height | Print Time | Material Used |
|-----------|--------------|------------|---------------|
| 25mm | 0.2mm | ~5 min | <2g |
| 32mm | 0.1mm | ~8 min | <4g |  
| 42mm | 0.1mm | ~10 min | <6g |
| 50mm | 0.2mm | ~12 min | <8g |

## Assembly Instructions

### With Magnets

1. **Print the base** with magnet hole
2. **Test fit magnet** - it should sit flush or slightly recessed
3. **Apply small amount of superglue** to magnet hole
4. **Insert magnet** ensuring proper polarity
5. **Press firmly** and allow to cure
6. **Attach to miniature** with plastic glue or superglue

### Without Magnets

1. **Print the base** solid (no magnet hole)
2. **Sand lightly** if needed for smooth finish  
3. **Apply glue** to miniature's existing base
4. **Press together** and hold until set

## Magnet Recommendations

### Popular Magnet Sizes

| Diameter | Thickness | Strength | Use Case |
|----------|-----------|----------|----------|
| 6mm | 2mm | Light | Small miniatures |
| 8mm | 2mm | Medium | Standard infantry |
| 10mm | 3mm | Strong | Large miniatures |
| 12mm | 3mm | Very Strong | Heavy models |

### Where to Buy

- **Amazon** - Neodymium disc magnets
- **K&J Magnetics** - Professional grade
- **Local electronics stores** - Often cheaper
- **eBay** - Bulk quantities

!!! tip "Magnet Polarity"
    Mark one side of your magnets with a Sharpie to ensure consistent polarity across all your bases!

## Troubleshooting

### Common Issues

**Magnet doesn't fit**
- Increase `magnet_diameter` by 0.2-0.5mm
- Check your printer's dimensional accuracy

**Base too thin/thick**  
- Adjust `thickness` parameter
- Consider your miniature's proportions

**Rough surface finish**
- Reduce layer height to 0.1mm
- Ensure proper bed leveling

**STL file not generated**
- Check `do_export = True`
- Verify file permissions in output directory
- Look for error messages in terminal

### Design Tips

**Professional Results:**
- Use consistent thickness across all bases (e.g., 3mm)
- Match magnet sizes for uniform storage
- Consider adding small chamfers for comfort

**Batch Production:**
- Generate multiple sizes at once
- Use identical magnet specifications
- Print multiple bases per plate

## File Location

```
src/model123d/base_plate/
├── base_plate_{identifier}_{size}_{parameters}.py
├── README.md
├── _output/          # Generated STL files
└── images/          # Photos and screenshots
```

## Next Steps

- Try the [Belt-A Phone Pouch](belta.md) for a more complex model
- Explore [Frame Hangers](frame-hanger.md) for household applications  
- Learn about [Development](../development/contributing.md) to create your own models

---

*Perfect bases for your epic adventures! ⚔️*
