# Project Structure

Understanding how Model123d is organized will help you navigate the codebase and find the models you need.

## Repository Layout

```
model123d/
├── 📄 README.md                    # Project overview
├── 📄 pyproject.toml              # Python project configuration
├── 📄 poetry.lock                 # Dependency lock file
├── 📄 mkdocs.yml                  # Documentation configuration
├── 📁 docs/                       # Documentation source (this site!)
├── 📁 print/                      # Ready-to-print 3MF files
├── 📁 src/                        # Source code
│   ├── 📁 assemble123d/           # Assembly and multi-part models
│   ├── 📁 material123d/           # Material and texture generation
│   └── 📁 model123d/              # Main model collection
└── 📁 tests/                      # Test files
```

## Model Categories

The main models are organized in `src/model123d/` by category:

### 🎲 Gaming & Miniatures
- **`base_plate/`** - Hexagonal and circular bases for tabletop gaming
- **`games/`** - Gaming accessories and components

### 📱 Phone & Electronics  
- **`belta/`** - "Belt-A" tactical phone pouches (Expanse-inspired)
- **`cmf_phone_pro/`** - CMF Phone Pro specific accessories
- **`recorder/`** - Audio recorder sleeves and cases

### 🏠 Household Items
- **`kitchen/`** - Kitchen tools and utensils
- **`frame_hanger/`** - Picture frame wall mounts  
- **`trash_bin_foot/`** - IKEA trash bin replacement feet

### 🔧 Tools & Repair
- **`repair/`** - Repair tools and fixtures
- **`trailer_plug/`** - Automotive trailer plug tools

### 🏗️ Architectural
- **`roof/`** - Roof models with chimneys and details

### 📚 Learning Resources
- **`examples/`** - Usage examples and tutorials

## Model Directory Structure

Each model category follows a consistent structure:

```
base_plate/                         # Model category
├── 📄 README.md                   # Category documentation
├── 📄 base_plate_{template}.py    # Main model script
├── 📁 _output/                    # Generated STL/3MF files
├── 📁 images/                     # Screenshots and photos
├── 📄 parameter.py                # Parameter definitions (some models)
├── 📄 helper.py                   # Utility functions (some models)
└── 📄 export.py                   # Export utilities (some models)
```

### File Naming Convention

Model files use template-based naming for flexibility:

```
{model_name}_{identifier}_{size}_{parameters}.py
```

**Examples:**
- `base_plate_Hexagonal_42.0_4.5_10.0.py`
- `frame_hanger_wall_mount_60x30mm.py`  
- `recorder_sleeve_cut.py`

**Template Variables:**
- `{identifier}` - Model variant (e.g., "Hexagonal", "Circular", "Large")
- `{size}` - Primary dimension in mm
- `{parameters}` - Additional parameter values

## Core Components

### Parameters Class

Each model defines its parameters using Python dataclasses:

```python
@dataclass
class P:
    """Parameters for the model."""
    do_export: bool = True
    do_pattern: bool = False
    size: float = 42.0 * mm
    thickness: float = 4.5 * mm
    # ... more parameters
```

### Model Creation

Models are built using build123d's declarative API:

```python
with BuildPart() as model:
    with BuildSketch() as sketch:
        # Create 2D geometry
        Circle(P.size / 2)
    extrude(amount=P.thickness)
    # Add features, fillets, etc.
```

### Export Logic

Most models include export functionality:

```python
if P.do_export:
    exporter = Mesher()
    exporter.add_shape(model.part)
    exporter.write(Path(__file__).parent / "output.stl")
```

## Special Directories

### 📁 `_output/`
Generated files from model scripts:
- **STL files** - Standard triangle mesh format for 3D printing
- **3MF files** - Multi-material format with color information
- **STEP files** - CAD interchange format (occasional)

### 📁 `images/`
Visual documentation:
- **Screenshots** from VS Code viewer
- **Printed photos** showing real-world results
- **Assembly instructions** for multi-part models

### 📁 `print/`
Ready-to-print files in the repository root:
- **Curated selection** of popular models
- **Tested parameters** known to print well
- **Multi-part assemblies** combined into single 3MF files

## Dependencies and Imports

### Common Imports

Most models start with these imports:

```python
from build123d import *                    # Core CAD functionality
from build123d import MM as mm            # Unit definitions
from ocp_vscode import show               # VS Code visualization
from dataclasses import dataclass        # Parameter definitions
from pathlib import Path                  # File operations
from rich.console import Console          # Pretty terminal output
```

### Local Imports

Some models have shared utilities:

```python
from parameter import Parameters          # Shared parameter definitions
from helper import debug, define, create_name
from export import export_all            # Export utilities
```

## Development Patterns

### Standard Model Template

```python
"""
Model description and metadata
"""

# [Imports] - External and local dependencies
# [Parameters] - @dataclass with model parameters
# [Constants] - Global variables and settings
# [Helper Functions] - Utility functions
# [Model Creation] - Main build123d code
# [Visualization] - show() calls for VS Code
# [Export] - File output logic
```

### Parameter Organization

Parameters are grouped logically:

```python
@dataclass
class P:
    # Export settings
    do_export: bool = True
    do_pattern: bool = False
    
    # Dimensions
    size: float = 42.0 * mm
    thickness: float = 4.5 * mm
    
    # Features
    do_magnet: bool = True
    magnet_diameter: float = 10.0 * mm
    
    # Advanced options
    do_fillet: bool = True
    show_debug: bool = False
```

## Navigation Tips

### Finding Models

1. **Browse by category** in `src/model123d/`
2. **Check README files** in each directory for details
3. **Look at `_output/`** to see what's already generated
4. **Search for keywords** in file names

### Understanding Relationships

- **Template files** contain `{identifier}` placeholders
- **Specific files** have filled-in parameters  
- **Helper modules** are shared across related models
- **Export utilities** handle file generation consistently

## Next Steps

Now that you understand the structure:

1. 🎯 **Explore specific models** - Pick a category that interests you
2. 🔍 **Read the README files** in each model directory
3. 🛠️ **Try modifying parameters** to see how models change
4. 📚 **Study the examples** to understand advanced techniques

Ready to dive deeper? Check out the [Base Plates](../models/base-plates.md) documentation for a detailed walkthrough of a complete model!
