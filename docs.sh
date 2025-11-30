#!/bin/bash
# MkDocs development helper script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

echo_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

echo_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo_error "uv is not installed. Please install it first:"
    echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Function to install dependencies
install_deps() {
    echo_info "Installing documentation dependencies..."
    uv sync --extra docs
    echo_info "Dependencies installed!"
}

# Function to serve documentation locally  
serve() {
    echo_info "Starting MkDocs development server..."
    echo_info "Open http://127.0.0.1:8000 in your browser"
    echo_info "Press Ctrl+C to stop the server"
    uv run mkdocs serve
}

# Function to build documentation
build() {
    echo_info "Building documentation..."
    uv run mkdocs build --strict
    echo_info "Documentation built in ./site/"
}

# Function to deploy to GitHub Pages (for maintainers)
deploy() {
    echo_warn "This will deploy to GitHub Pages. Are you sure? (y/N)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        echo_info "Deploying to GitHub Pages..."
        uv run mkdocs gh-deploy --strict
        echo_info "Deployed!"
    else
        echo_info "Deployment cancelled."
    fi
}

# Function to create new model documentation
new_model() {
    if [ -z "$1" ]; then
        echo_error "Please provide a model name"
        echo "Usage: $0 new-model <model-name>"
        exit 1
    fi
    
    MODEL_NAME="$1"
    DOC_FILE="docs/models/${MODEL_NAME}.md"
    
    if [ -f "$DOC_FILE" ]; then
        echo_error "Documentation file already exists: $DOC_FILE"
        exit 1
    fi
    
    echo_info "Creating documentation for model: $MODEL_NAME"
    
    cat > "$DOC_FILE" << EOF
# ${MODEL_NAME^}

Brief description of what this model creates.

## Overview

Detailed description of the model's purpose and features.

### Key Features

- ✅ Feature 1
- ✅ Feature 2
- ✅ Feature 3

## Parameters

\`\`\`python
@dataclass
class P:
    """Parameters for the model."""
    do_export: bool = True
    # Add your parameters here
\`\`\`

## Usage Examples

### Basic Usage

\`\`\`python
# Example usage code
\`\`\`

## Print Settings

| Setting | Value | Notes |
|---------|-------|-------|
| Material | PETG | Recommended |
| Layer Height | 0.2mm | Standard quality |
| Infill | 20% | Adequate strength |

## File Location

\`\`\`
src/model123d/${MODEL_NAME}/
├── ${MODEL_NAME}_{identifier}.py
├── README.md
└── _output/
\`\`\`

---

*Add your model description here! 🎯*
EOF
    
    echo_info "Created: $DOC_FILE"
    echo_info "Don't forget to add it to mkdocs.yml navigation!"
}

# Function to check for broken links
check_links() {
    echo_info "Building documentation and checking for issues..."
    uv run mkdocs build --strict
    echo_info "Build successful - no broken links found!"
}

# Main script logic
case "${1:-help}" in
    "install"|"setup")
        install_deps
        ;;
    "serve"|"dev")
        serve
        ;;
    "build")
        build
        ;;
    "deploy")
        deploy
        ;;
    "new-model")
        new_model "$2"
        ;;
    "check"|"test")
        check_links
        ;;
    "help"|*)
        echo "MkDocs Helper Script for Model123d"
        echo ""
        echo "Usage: $0 <command>"
        echo ""
        echo "Commands:"
        echo "  install     Install documentation dependencies"
        echo "  serve       Start development server (with live reload)"
        echo "  build       Build static documentation"
        echo "  deploy      Deploy to GitHub Pages (maintainers only)"
        echo "  new-model   Create new model documentation template"
        echo "  check       Check for broken links and build issues"
        echo "  help        Show this help message"
        echo ""
        echo "Examples:"
        echo "  $0 install                 # Install dependencies"
        echo "  $0 serve                   # Start dev server"
        echo "  $0 new-model gear-box      # Create new model docs"
        echo ""
        ;;
esac
