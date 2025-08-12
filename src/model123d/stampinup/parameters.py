# -*- coding: utf-8 -*-
"""
Parameters module for stampinup models.

This module provides parameter classes and constants for generating 3D models.
This is currently a local implementation, but will be migrated to use noah123d.

----
file-name:       parameters.py
file-uuid:       generated-uuid
description:     Parameter classes and constants for stampinup 3D models
author:          felix@42sol.eu
project:
    name:        model123d
    uuid:        fe521ba0-4ad7-484d-9386-26de71379e15
    url:         https://www.github.com/42sol/model123d

TODO: Migrate to use noah123d.parameters once the noah123d package is updated
"""

# %% [Imports]
from dataclasses import dataclass, fields, field
from pathlib import Path
from typing import Dict, Any, Optional

# %% [Constants]
no = False 
yes = True
mm = 1

# %% [Functions]
def debug(msg):
    """Print debug message if show_debug is True"""
    # Import here to avoid circular imports
    try:
        from rich import print as rich_print
        if hasattr(Parameters, 'show_debug') and Parameters.show_debug:
            rich_print(f"[blue]DEBUG: {msg}[/blue]")
    except (ImportError, NameError, AttributeError):
        # Fallback if rich is not available or Parameters not yet defined
        print(f"DEBUG: {msg}")

def file_path():
    """Return the path to the current file"""
    return Path(__file__).parent.resolve()



# %% [Parameters]
@dataclass
class Parameters:
    """Base parameters class for all models"""
    show_debug:    bool =    yes
    do_show:       bool =    yes
    do_export:     bool =    yes
    
    do_text:       bool =    no
    do_fillet:      bool =    yes
    export_folder: Path = file_path() / "_export"

    def __init__(self) -> Any:
        debug("Initializing core parameters")
        
    def __str__(self):
        """String representation of the parameters"""
        data = "Parameters:\n"
        for f in fields(self):
            value = getattr(self, f.name)
            desc = f.metadata.get("description", "")
            desc_str = f" ({desc})" if desc else ""
            data += f"  {f.name}: {value}{desc_str}\n"
        return data

    @classmethod
    def short_field(cls, default: Any, short_name: str, description: Optional[str] = None):
        """
        Create a dataclass field with short name metadata for compact naming.
        
        Args:
            default: Default value for the field
            short_name: Short identifier for compact file naming  
            description: Optional description of the parameter
        """
        metadata = {"short_name": short_name}
        if description:
            metadata["description"] = description
        return field(default=default, metadata=metadata)
    
    def name(self) -> str:
        """Generate a compact name using short field names from metadata"""
        parts = []
        for f in fields(self):
            if hasattr(f, 'metadata') and 'short_name' in f.metadata:
                short_name = f.metadata['short_name']
                value = getattr(self, f.name)
                # Format numbers to remove unnecessary decimals
                if isinstance(value, float) and value.is_integer():
                    value = int(value)
                parts.append(f"{short_name}={value}")
        
        params = "_".join(parts)
        
        # Add fillet info if enabled
        if hasattr(self, 'do_fillet') and self.do_fillet:
            params += "_filleted"

        params = f'__{params}' if params else '__default'
        return params

    def get_short_names(self) -> Dict[str, str]:
        """Get mapping of short names to field names"""
        short_names = {}

        for f in fields(self):
            if "short_name" in f.metadata:
                short_name = f.metadata.get("short_name", f.name)
                short_names[short_name] = f.name

        return short_names

    def export_path(self, filename: str) -> Path:
        """Generate full export path for a given filename"""
        name_parts = Path(filename)
        stem = name_parts.stem
        suffix = name_parts.suffix
        
        full_name = f"{stem}{self.name()}{suffix}"
        return self.export_folder / full_name

@dataclass
class ClipParameters(Parameters):
    """Parameters for the clip geometry."""
    length:       float = Parameters.short_field(20.0, "l0", "Overall length of the clip")
    width_inner:  float = Parameters.short_field( 6.0, "w1", "Inner width of the clip")
    height_inner: float = Parameters.short_field( 4.0, "h1", "Inner height of the clip")
    thickness:    float = Parameters.short_field( 5.0, "t0", "Wall thickness")
    fillet_radius: float = Parameters.short_field( 0.4, "fr", "Fillet radius for edges")

    def __init__(self) -> Any:
        super().__init__()
        debug("Initializing clip parameters")
