# README: Model123d

A 3D modeling collection of parametric models built with [build123d](https://build123d.readthedocs.io/) (Python-based OCCT). This project provides reusable, customizable 3D models for various applications designed by felix@42sol.

## 🎯 Project overview

**model123d** is a parametric 3D modeling collection. All models generate STL and some even 3MF files for 3D printing. 
All models are programmatically created using Python, making them easily customizable through parameter adjustments.

**Author:** Andreas **Felix** Häberle (felix@42sol.eu)  
**Repository:** [42sol-eu/model123d](https://github.com/42sol-eu/model123d)  
**License:** Mixed (see individual model notes)

## 🔧 Installation

### Prerequisites

- Python 3.12
- uv (recommended) or pip

### Using uv (recommended)

```bash
git clone https://github.com/42sol-eu/model123d.git
cd model123d
uv sync
```

### Using pip

```bash
git clone https://github.com/42sol-eu/model123d.git
cd model123d
pip install -r requirements.txt  # Or install dependencies manually
```

### Key dependencies

- **build123d** (>=0.9.1) - Python-based OCCT modeling library
- **ocp-vscode** (>=2.7.1) - VS Code integration for 3D visualization
- **rich** - Enhanced terminal output
- **lib3mf** - 3MF file format support
- **pillow** - Image processing

## 📁 Project structure

```
src/model123d/
├── base_plate/          # Miniature gaming bases (hexagonal/circular)
├── belta/              # "Belt-A" phone pouches (Expanse-inspired)
├── cmf_phone_pro/      # CMF Phone Pro accessories
├── examples/           # Usage examples and tutorials
├── frame_hanger/       # Picture frame wall mounts
├── games/              # Gaming accessories
├── kitchen/            # Kitchen tools and accessories
├── recorder/           # Audio recorder sleeves
├── repair/             # Repair and maintenance tools
├── roof/               # Architectural roof models
├── trailer_plug/       # Automotive trailer plug tools
└── trash_bin_foot/     # IKEA trash bin feet replacements
```

## 🚀 Quick start

### Running a model

Each model is a self-contained Python script with parameters at the top:

```bash
# Navigate to any model directory
cd src/model123d/base_plate/

# Run the parametric model
python base_plate_{identifier}_{size}_{parameters}.py
```

### Example: Creating a base plate

```python
from src.model123d.base_plate import base_plate_Hexagonal_42.0

# Parameters are defined in the script:
# P.size = 42.0 * mm          # Base diameter
# P.thickness = 4.5 * mm      # Base thickness  
# P.magnet_diameter = 10.0    # Magnet hole size
# P.do_export = True          # Generate STL file
```

### Customizing parameters

Edit the parameters at the top of each model file:

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
    type: str = "Circular"  # "Hexagonal" or "Circular"
```

## 🎯 Featured models

### 🎲 Base plates for miniatures
**Location:** `src/model123d/base_plate/`
- Hexagonal and circular bases for tabletop gaming
- Integrated magnet holes for magnetic storage
- Customizable size, thickness, and magnet dimensions
- **Printables:** [1314888](https://www.printables.com/model/1314888)

### 📱 Belt-A phone molle pouch - designed for CMF Phone 2
**Location:** `src/model123d/belta/`
- Tactical-style phone pouch inspired by *The Expanse*
- MOLLE-compatible attachment system
- Customizable front panel (fabric/leather)
- Designed for CMF Phone Pro but adaptable

### 🖼️ Frame hanger
**Location:** `src/model123d/frame_hanger/`
- Wall-mounted picture frame hangers
- Two-screw mounting system
- **Printables:** [1314877](https://www.printables.com/model/1314877-picture-frame-hanger-wall-mount)

### 🏠 IKEA trash bin feet
**Location:** `src/model123d/trash_bin_foot/`
- Replacement feet for IKEA HÖLASS trash bins
- Includes clamp mechanism
- Custom fit for specific bin models

## 🛠️ Development

### Adding a new model

1. Create a new directory under `src/model123d/your_model/`
2. Copy the template structure from an existing model
3. Implement your parametric design using build123d
4. Add parameter definitions and export functionality
5. Create a README.md with usage instructions

### Model template structure

```python
"""
file-name:      your_model_{identifier}.py
description:    Brief model description
project:        model123d
"""

# [Imports]
from build123d import *
from dataclasses import dataclass
from pathlib import Path

# [Parameters]
@dataclass
class P:
    """Parameters for your model."""
    do_export: bool = True
    # Add your parameters here

# [Model Creation]
with BuildPart() as your_part:
    # Your model code here
    pass

# [Export]
if P.do_export:
    exporter = Mesher()
    exporter.add_shape(your_part.part)
    exporter.write(Path(__file__).parent / "output.stl")
```

### VS Code integration

The project includes VS Code integration via `ocp-vscode`:

```python
from ocp_vscode import show
show(your_model)  # Visualize in VS Code
```

## 📋 Usage notes

### File naming convention

Models use template-based naming:
- `{identifier}` - Model variant (e.g., "Hexagonal", "Circular")
- `{size}` - Primary dimension
- `{parameters}` - Additional parameter values

### Export formats

- **STL** - Default format for 3D printing
- **3MF** - Multi-material format with color information
- **STEP** - CAD interchange format

### Print settings

Most models are designed for:
- **Material:** PETG (recommended), PLA, ABS
- **Layer Height:** 0.1-0.2mm
- **Infill:** 20%
- **Supports:** Auto-generated where needed

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your model with documentation
4. Test the model generation and export
5. Submit a pull request

### Guidelines

- Follow the existing code structure and naming conventions
- Include parameter documentation
- Add usage examples and print settings
- Test models with different parameter combinations

## 📜 License

- **Personal/Non-commercial use:** Generally permitted
- **Commercial use:** Contact the designer (felix@42sol.eu)
- **Individual models:** May have specific licensing (see model READMEs)

## 🔗 Related projects

- **[build123d](https://github.com/gumyr/build123d)** - Core modeling library
- **[ocp-vscode](https://github.com/bernhard-42/ocp-vscode)** - VS Code 3D visualization
- **[lib3mf](https://github.com/3MFConsortium/lib3mf)** - 3MF file format support

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/42sol-eu/model123d/issues)
- **Email:** felix@42sol.eu
- **Documentation:** Individual model READMEs

---

*Built with Python 🐍 and build123d 🔧 | Ready for the 23rd century ⭐**