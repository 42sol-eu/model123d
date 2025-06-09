# -*- coding: utf-8 -*-
"""
----
file-name:      external.py
file-uuid:      bd40d245-9999-48fb-811c-21321a842687
description:   export external parts for the belta project, use `_import`folder.

project:
    name:       model123d
    uuid:       a0b40edb-6c25-41b9-878f-6bf97bfcf0a2
    url:        https://www.github.com/42sol/model123d
"""

# [Imports]
from rich import print  # [docs](https://rich.readthedocs.io)
from rich.console import Console
from pathlib import Path  # [docs](https://docs.python.org/3/library/pathlib.html)

# [Parameters]

# [Global_Variables]
console = Console()

# [Code]
# [Imports]
from build123d import *
from pathlib import Path

# [Local Imports]
from helper import *

# [Functions]


def load_backplate_original(
    file_name: str = "cmf_phone_2_pro_universal_cover_2.stl",
) -> object:
    """
    Loads and imports a backplate STL file, positions it, and defines its appearance.
    This function attempts to import an STL file representing a backplate from a predefined path,
    move it to a specific location, and define its color and identifier for further use. If the import
    fails, it logs the error. The function returns the imported backplate object.
    Returns:
        object: The imported and positioned backplate object, or None if import fails.
    """

    debug("Loading backplate")
    # Import an STL part (replace with your STL file path)
    stl_path = Path(__file__).parent / "_import" / file_name
    if not stl_path.exists():
        debug(f"STL file {stl_path} does not exist.")
        return None
    try:
        backplate = import_stl(stl_path)
        backplate.move(loc=Location((-P.body_width - 8, -23.35, P.body_extrude - 0.8)))
        # .rotate(Axis.Z, 45)  # Rotate the backplate to match the orientation
        define(backplate, "#ffffffdd", "backplate_imported")
        debug(f"Imported STL part from {stl_path}. {type(backplate)}")

    except Exception as e:
        debug(f"Failed to import STL: {e}")

    return backplate


def load_imports():
    """Load and return all necessary imports for the project.
    Args:
        None
    Returns:
        dict: A dictionary containing the imported objects, including the original backplate.
    """
    objects = {}
    import_backplate = load_backplate_original()
    objects["original_backplate"] = import_backplate

    return objects


# [Main]

if __name__ == "__main__":
    from ocp_vscode import show

    objects = load_imports()
    show(objects, glass=yes)

# [End of file]
