# Installation

Get started with **Model123d** by setting up your development environment and installing the necessary dependencies.

## Prerequisites

- **Python 3.12**
- **uv** (recommended) or pip
- **Git** for cloning the repository

## Installation Methods

### Using uv (Recommended)

uv is the recommended way to manage dependencies and virtual environments for this project.

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone https://github.com/42sol-eu/model123d.git
cd model123d

# Install dependencies and create virtual environment
uv sync
```

!!! tip "Why uv?"
    uv is an extremely fast Python package and project manager written in Rust. It automatically manages virtual environments and dependency resolution, making it much faster than traditional tools while maintaining compatibility with pip and pyproject.toml standards.

### Using pip

If you prefer to use pip, you can install the dependencies manually:

```bash
# Clone the repository
git clone https://github.com/42sol-eu/model123d.git
cd model123d

# Create and activate a virtual environment (recommended)
python -m venv model123d-env
source model123d-env/bin/activate  # On Windows: model123d-env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

!!! warning "Virtual Environment"
    Always use a virtual environment to avoid conflicts with other Python packages on your system.

## Key Dependencies

The project relies on several important libraries:

| Package | Version | Purpose |
|---------|---------|---------|
| **build123d** | >=0.9.1 | Python-based OCCT modeling library - the core of our 3D modeling |
| **ocp-vscode** | >=2.7.1 | VS Code integration for 3D visualization and debugging |
| **rich** | >=14.1.0 | Enhanced terminal output with colors and formatting |
| **lib3mf** | >=2.4.1 | Support for 3MF file format (multi-material 3D models) |
| **trimesh** | >=4.7.1 | Mesh processing and manipulation |
| **pillow** | >=11.3.0 | Image processing for textures and materials |

## VS Code Setup (Optional but Recommended)

For the best development experience, we recommend using Visual Studio Code with the OCP CAD Viewer extension:

1. **Install VS Code**: Download from [code.visualstudio.com](https://code.visualstudio.com/)

2. **Install the OCP CAD Viewer extension**:
   ```bash
   # Install the extension file if provided
   code --install-extension ocp-cad-viewer-2.8.1.vsix
   ```

3. **Open the project in VS Code**:
   ```bash
   code .
   ```

!!! info "3D Visualization"
    The OCP CAD Viewer extension allows you to visualize 3D models directly in VS Code, making development and debugging much more efficient.

## Verification

Verify your installation by running a simple model:

```bash
# Navigate to a model directory
cd src/model123d/base_plate/

# Run a model (this will generate an STL file)
python base_plate_Hexagonal_42.0_4.5_10.0.py
```

If everything is set up correctly, you should see:
- Rich-formatted output in your terminal
- An STL file generated in the `_output` directory
- 3D visualization in VS Code (if using the extension)

## Troubleshooting

### Common Issues

**Import Error: No module named 'build123d'**
```bash
# Reinstall dependencies
uv sync
```

**VS Code not showing 3D models**
- Ensure the OCP CAD Viewer extension is installed and enabled
- Check that you're running the Python script within VS Code
- Verify the `ocp-vscode` package is installed

**Permission errors on macOS/Linux**
```bash
# You might need to install some system dependencies
# On macOS with Homebrew:
brew install opencascade

# On Ubuntu/Debian:
sudo apt-get install libocct-dev
```

### Getting Help

If you encounter issues:

1. Check the [GitHub Issues](https://github.com/42sol-eu/model123d/issues) for similar problems
2. Review the [build123d documentation](https://build123d.readthedocs.io/)
3. Contact the maintainer at [felix@42sol.eu](mailto:felix@42sol.eu)

## Next Steps

Once you have everything installed:

1. 📖 Read the [Quick Start Guide](quick-start.md)
2. 🏗️ Explore the [Project Structure](project-structure.md)  
3. 🎯 Try creating your first [Base Plate](../models/base-plates.md)
