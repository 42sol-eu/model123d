# Contributing to Model123d

Thank you for your interest in contributing to Model123d! This guide will help you get started with adding new models, fixing bugs, and improving the project.

## 🚀 Quick Start for Contributors

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR-USERNAME/model123d.git
cd model123d

# Add the original repository as upstream
git remote add upstream https://github.com/42sol-eu/model123d.git
```

### 2. Set Up Development Environment

```bash
# Install dependencies
uv sync

# Verify installation
cd src/model123d/examples/
uv run python show_objects_1.py
```

### 3. Create a Feature Branch

```bash
git checkout -b feature/my-awesome-model
# or
git checkout -b fix/issue-description
```

## 🏗️ Adding a New Model

### Step 1: Create Model Directory

```bash
mkdir src/model123d/your_model_name/
cd src/model123d/your_model_name/
```

### Step 2: Use the Model Template

Create your main model file using this template:

```python
"""
----
file-name:      your_model_{identifier}.py
file-uuid:      [generate a UUID4]
description:    Brief description of what this model creates

project:
    name:       model123d
    uuid:       a0b40edb-6c25-41b9-878f-6bf97bfcf0a2
    url:        https://www.github.com/42sol-eu/model123d
"""

# [Imports]
from build123d import *
from build123d import MM as mm
from ocp_vscode import show
from dataclasses import dataclass
from pathlib import Path
import sys
from rich.console import Console

# [Setup]
console = Console()
objects = []

# [Constants]
no, yes = False, True

# [Helper Functions]
def debug(msg: str):
    """Print debug message if enabled"""
    if P.show_debug:
        console.print(f"[blue]DEBUG[/blue] {msg}")

def define(obj, color="#ff0000", name=""):
    """Define object properties for visualization"""
    if hasattr(obj, 'color'):
        obj.color = color
    if hasattr(obj, 'name'):
        obj.name = name
    objects.append(obj)

# [Parameters]
@dataclass
class P:
    """Parameters for your model."""
    # Export settings
    do_export: bool = yes
    show_debug: bool = no
    
    # Model dimensions
    width: float = 50.0 * mm
    height: float = 30.0 * mm
    thickness: float = 3.0 * mm
    
    # Features
    do_fillet: bool = yes
    fillet_radius: float = 1.0 * mm

# [Model Creation]
if yes or __name__ == "__main__":
    debug("Creating your model")
    
    with BuildPart() as your_model:
        # Create your 3D geometry here
        Box(P.width, P.height, P.thickness)
        
        if P.do_fillet:
            fillet(your_model.edges(), radius=P.fillet_radius)
    
    define(your_model, "#00aa00ff", "Your Model")
    
    # [Visualization]
    show(*objects)
    
    # [Export]
    if P.do_export:
        debug("Exporting model")
        export_name = __file__.replace('.py', '.stl')
        export_path = Path(__file__).parent / "_output" / Path(export_name).name
        
        console.log(f"[green]Model exported to {export_path}[/green]")
        exporter = Mesher()
        exporter.add_shape(your_model.part)
        exporter.write(export_path)
        del exporter

# [End of file]
```

### Step 3: Create Supporting Files

**README.md**
```markdown
# Your Model Name

Brief description of what this model creates and its purpose.

## Usage

Explain how to use the model, customize parameters, and what it's good for.

## Parameters

Document the main parameters users can adjust.

## Print Settings

Recommended print settings and material choices.
```

**Create output directory**
```bash
mkdir _output
```

### Step 4: Test Your Model

```bash
# Test the model generation
python your_model_template.py

# Check that STL file is created
ls _output/
```

## 📝 Code Style Guidelines

### Python Code Style

We use [Black](https://black.readthedocs.io/) for code formatting:

```bash
# Format your code before committing
uv run black src/
```

### Documentation Style

- Use **Markdown** for all documentation
- Include **code examples** with syntax highlighting
- Add **parameter tables** for complex models
- Use **admonitions** (tips, warnings, info) appropriately

### Naming Conventions

**Files:**
- Use `snake_case` for Python files
- Template files: `model_name_{identifier}.py`
- Helper modules: `helper.py`, `export.py`, `parameter.py`

**Classes and Variables:**
- Parameters class: `P` (dataclass)
- Build123d objects: descriptive names (`base_plate`, `mounting_hole`)
- Constants: `UPPER_CASE` or `yes/no` for booleans

## 🧪 Testing Your Contribution

### Automated Testing

Run the test suite to ensure your changes don't break existing functionality:

```bash
# Run all tests
python -m pytest tests/

# Run specific test
python -m pytest tests/test_base_plate.py
```

### Manual Testing

1. **Generate your model** - Ensure STL files are created correctly
2. **Test in slicer** - Import STL and verify it slices properly  
3. **Print a sample** - Verify real-world functionality
4. **Test different parameters** - Try various parameter combinations

### Documentation Testing

```bash
# Test documentation builds
mkdocs serve

# Check for broken links
mkdocs build --strict
```

## 📚 Documentation Requirements

### Model Documentation

Each new model should include:

1. **README.md** in the model directory
2. **Parameter documentation** with examples
3. **Print settings** and material recommendations
4. **Usage scenarios** and examples
5. **Assembly instructions** if multi-part

### API Documentation

If you add new helper functions or classes:

```python
def your_function(param1: str, param2: float = 1.0) -> bool:
    """
    Brief description of what the function does.
    
    Args:
        param1: Description of first parameter
        param2: Description of second parameter with default
        
    Returns:
        Description of return value
        
    Example:
        ```python
        result = your_function("test", 2.5)
        ```
    """
    pass
```

## 🐛 Bug Reports and Issues

### Reporting Bugs

When reporting bugs, please include:

1. **Python version** and operating system
2. **build123d version** (`uv pip list | grep build123d`)
3. **Complete error message** and traceback
4. **Steps to reproduce** the issue
5. **Expected vs actual behavior**

### Issue Labels

We use these labels to categorize issues:

- 🐛 `bug` - Something isn't working
- ✨ `enhancement` - New feature or request  
- 📚 `documentation` - Documentation improvements
- 🎯 `model-request` - Request for new model
- 🛠️ `maintenance` - Code maintenance and refactoring

## 🔄 Pull Request Process

### Before Submitting

1. **Update documentation** for any new features
2. **Add tests** for new functionality
3. **Run code formatter**: `uv run black src/`
4. **Test thoroughly** with different parameters
5. **Update CHANGELOG** if applicable

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New model
- [ ] Documentation update
- [ ] Code refactoring

## Testing
- [ ] Tested model generation
- [ ] Tested in slicer
- [ ] Documentation builds correctly
- [ ] All tests pass

## Screenshots
Include screenshots of generated models if applicable
```

### Review Process

1. **Automated checks** must pass (linting, tests)
2. **Maintainer review** for code quality and design
3. **Community feedback** for new models
4. **Documentation review** for completeness

## 🏆 Recognition

Contributors are recognized in:

- **CONTRIBUTORS.md** file
- **Model documentation** (for model creators)
- **Release notes** for significant contributions

## 📞 Getting Help

### Development Questions

- **GitHub Discussions** - For general questions
- **GitHub Issues** - For specific problems
- **Email maintainer** - felix@42sol.eu for private questions

### Learning Resources

- **[build123d Documentation](https://build123d.readthedocs.io/)** - Core modeling library
- **[OpenCASCADE Documentation](https://dev.opencascade.org/)** - Underlying geometry kernel
- **[VS Code Extensions](https://marketplace.visualstudio.com/items?itemName=bernhard-42.ocp-cad-viewer)** - 3D visualization

## 🎯 Model Quality Standards

### Design Principles

- **Parametric** - All dimensions should be adjustable
- **Print-friendly** - Consider overhang, support, and orientation
- **Well-documented** - Clear parameter descriptions
- **Tested** - Verify the model prints successfully

### Code Quality

- **Readable** - Use clear variable names and comments
- **Modular** - Separate complex logic into functions
- **Robust** - Handle edge cases and invalid parameters
- **Consistent** - Follow existing patterns and conventions

## 🚀 Advanced Contributions

### New Categories

If you want to add a new model category:

1. **Propose the category** in GitHub Discussions
2. **Create the directory structure**
3. **Add category documentation** 
4. **Include 2-3 example models**
5. **Update main navigation**

### Core Improvements

For improvements to the build system or core utilities:

1. **Discuss the change** before starting work
2. **Maintain backward compatibility** where possible
3. **Update all affected models**
4. **Provide migration guide** if needed

---

**Ready to contribute? Start with a simple model and work your way up! 🚀**

*Thank you for helping make Model123d better for everyone!*
