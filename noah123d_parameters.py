# -*- coding: utf-8 -*-
"""
Reusable parameter classes for build123d projects.

This module provides base parameter classes and utilities for managing
parameters across different 3D modeling projects.

This file is designed to be added to the noah123d package.

----
file-name:       parameters.py (for noah123d package)
file-uuid:       noah123d-parameters-uuid
description:     Reusable parameter classes and utilities for build123d projects
author:          felix@42sol.eu
project:
    name:        noah123d
    url:         https://github.com/42sol-eu/noah123d
"""

# %% [Imports]
from dataclasses import dataclass, fields, field
from pathlib import Path
from typing import Dict, Any, Optional

# %% [Constants]
no = False
yes = True
mm = 1

# %% [Utilities]
def short_field(default: Any, short_name: str, description: Optional[str] = None):
    """
    Create a dataclass field with short name metadata for compact naming.
    
    Args:
        default: Default value for the field
        short_name: Short identifier for compact file naming
        description: Optional description of the parameter
    
    Returns:
        dataclass field with metadata
    """
    metadata = {"short_name": short_name}
    if description:
        metadata["description"] = description
    return field(default=default, metadata=metadata)

# %% [Base Classes]
@dataclass
class BaseParameters:
    """
    Base parameters class for all 3D models.
    
    Provides common functionality for parameter management including:
    - Debug output control
    - Export settings
    - Compact naming based on field metadata
    - String representation
    """
    show_debug: bool = yes
    do_show: bool = yes
    do_export: bool = yes
    do_fillet: bool = no
    export_folder: Path = field(default_factory=lambda: Path.cwd() / "_export")

    def __post_init__(self):
        """Initialize after dataclass creation"""
        if hasattr(self, '_debug_msg'):
            self._debug(self._debug_msg)

    def _debug(self, msg: str):
        """Print debug message if show_debug is True"""
        if self.show_debug:
            try:
                from rich import print
                print(f"[blue]DEBUG: {msg}[/blue]")
            except ImportError:
                print(f"DEBUG: {msg}")

    def __str__(self):
        """String representation of the parameters"""
        data = f"{self.__class__.__name__}:\n"
        for f in fields(self):
            value = getattr(self, f.name)
            desc = f.metadata.get("description", "")
            desc_str = f" ({desc})" if desc else ""
            data += f"  {f.name}: {value}{desc_str}\n"
        return data

    def name(self) -> str:
        """
        Generate a compact name using short field names from metadata.
        
        Returns:
            Compact string suitable for file naming
        """
        parts = []
        for f in fields(self):
            if hasattr(f, 'metadata') and 'short_name' in f.metadata:
                short_name = f.metadata['short_name']
                value = getattr(self, f.name)
                # Format numbers to remove unnecessary decimals
                if isinstance(value, float) and value.is_integer():
                    value = int(value)
                parts.append(f"{short_name}{value}")
        
        params = "_".join(parts)
        
        # Add fillet info if enabled
        if hasattr(self, 'do_fillet') and self.do_fillet:
            params += "_filleted"

        return f'__{params}' if params else '__default'

    def get_short_names(self) -> Dict[str, str]:
        """Get mapping of short names to field names"""
        return {f.metadata.get("short_name", f.name): f.name 
                for f in fields(self) if "short_name" in f.metadata}

    def get_field_descriptions(self) -> Dict[str, str]:
        """Get mapping of field names to descriptions"""
        return {f.name: f.metadata.get("description", "") 
                for f in fields(self) if "description" in f.metadata}

    def export_path(self, filename: str) -> Path:
        """
        Generate full export path for a given filename.
        
        Args:
            filename: Base filename (extension will be preserved)
            
        Returns:
            Full path including export folder and parameter-based naming
        """
        name_parts = Path(filename)
        stem = name_parts.stem
        suffix = name_parts.suffix
        
        full_name = f"{stem}{self.name()}{suffix}"
        return self.export_folder / full_name

# %% [Specialized Parameter Classes]
@dataclass
class GeometricParameters(BaseParameters):
    """Base class for geometric parameters with common dimensions"""
    length: float = short_field(10.0, "l", "Length dimension")
    width: float = short_field(10.0, "w", "Width dimension") 
    height: float = short_field(10.0, "h", "Height dimension")
    fillet_radius: float = short_field(0.5, "fr", "Fillet radius")

@dataclass
class MaterialParameters(BaseParameters):
    """Base class for material-related parameters"""
    thickness: float = short_field(2.0, "t", "Material thickness")
    clearance: float = short_field(0.2, "c", "Clearance tolerance")
    draft_angle: float = short_field(0.0, "da", "Draft angle in degrees")

# %% [Factory Functions]
def create_parameter_class(name: str, base_class=BaseParameters, **field_definitions):
    """
    Factory function to dynamically create parameter classes.
    
    Args:
        name: Name of the new class
        base_class: Base class to inherit from
        **field_definitions: Field definitions as kwargs
        
    Returns:
        New dataclass type
    """
    # Convert field definitions to dataclass fields
    annotations = {}
    defaults = {}
    
    for field_name, field_def in field_definitions.items():
        if isinstance(field_def, tuple):
            field_type, default_value = field_def[:2]
            short_name = field_def[2] if len(field_def) > 2 else field_name[:2]
            description = field_def[3] if len(field_def) > 3 else ""
            
            annotations[field_name] = field_type
            defaults[field_name] = short_field(default_value, short_name, description)
        else:
            annotations[field_name] = type(field_def)
            defaults[field_name] = field_def
    
    # Create the new class
    new_class = type(name, (base_class,), {
        '__annotations__': annotations,
        **defaults
    })
    
    return dataclass(new_class)
