# -*- coding: utf-8 -*-
"""
----
file-name:      export.py
file-uuid:      ea868958-edc2-4479-8ca1-d9099fcd4740
description:   Export functions for the belta project.

project:
    name:       model123d
    uuid:       a0b40edb-6c25-41b9-878f-6bf97bfcf0a2
    url:        https://www.github.com/42sol/model123d
"""

# [Imports]
from build123d import Part, Mesher  ##|md: [docs](https://build123d.readthedocs.io)
from rich import print  ##############|md: [docs](https://rich.readthedocs.io)
from rich.console import Console  ####|md:
from pathlib import (
    Path,
)  ##|md: [docs](https://docs.python.org/3/library/pathlib.html)

# [Local Imports]
from parameter import Parameters
from helper import debug, create_name

# [Parameters]
# None

# [Global_Variables]
# None

# [Code]

# [Functions]


def export_parts_to_stl(file_path: str, parts: list[Part]) -> str:
    """
    Exports a list of Parts to an STL file.
    If `file_path` is a list or tuple, constructs the file name using the first element as the base path
    and the remaining elements as suffixes, joined by underscores. Otherwise, uses `file_path` directly.

    Args:
        file_path (str | list | tuple): The path to the output STL file, or a list/tuple where the first element
            is the base path and the remaining elements are used as suffixes for the file name.
        parts (list[Part]): A list of build123d.Part objects to export.

    Returns:
        file_path (str): The path to the exported STL file, empty string if nothing was exported.
    """
    if isinstance(file_path, (list, tuple)):
        base_path = file_path[0]
        suffix = "_".join(str(s) for s in file_path[1:])
        file_path = create_name(base_path, suffix, "stl")
        print(f"Exporting to {file_path}")

    exporter = Mesher()
    for part in parts:
        exporter.add_shape(part)
    exporter.write(file_path)

    if exporter.has_errors():
        print(f"Errors occurred during export: {exporter.errors()}")
        file_path = ""
    else:
        print(f"Exported {len(parts)} parts to {file_path}")

    return file_path


def export_all(file_path: str, parts: list[Part]) -> str:
    """
    Exports a list of Parts to an STL file.
    If `file_path` is a list or tuple, constructs the file name using the first element as the base path
    and the remaining elements as suffixes, joined by underscores. Otherwise, uses `file_path` directly.

    Args:
        file_path (str | list | tuple): The path to the output STL file, or a list/tuple where the first element
            is the base path and the remaining elements are used as suffixes for the file name.
        parts (list[Part]): A list of build123d.Part objects to export.

    Returns:
        file_path (str): The path to the exported STL file, empty if nothing was exported.
    """
    if isinstance(file_path, (list, tuple)):
        base_path = file_path[0]
        suffix = "_".join(str(s) for s in file_path[1:])
        file_path = create_name(base_path, suffix, "stl")
        print(f"Exporting to {file_path}")
    exporter = Mesher()
    for part in parts:
        exporter.add_shape(part)
    exporter.write(file_path)

    if exporter.has_errors():
        print(f"Errors occurred during export: {exporter.errors()}")
        file_path = ""
    else:
        print(f"Exported {len(parts)} parts to {file_path}")

    return file_path


# [End of file]
