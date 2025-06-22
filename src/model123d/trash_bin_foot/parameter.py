# -*- coding: utf-8 -*-
"""
----
file-name:      parameter.py
file-uuid:      6503fe38-5d6c-4435-a54e-ac22e96465a6
description:   Define the parameters for the belta for cmf_phone_2_pro project.

project:
    name:       model123d
    uuid:       a0b40edb-6c25-41b9-878f-6bf97bfcf0a2
    url:        https://www.github.com/42sol/model123d
"""

# [Imports]
from rich import print  # [docs](https://rich.readthedocs.io)
from rich.console import Console
from pathlib import Path  # [docs](https://docs.python.org/3/library/pathlib.html)

# [Local Imports]
from helper import *

# [Constants]
no = False
yes = True
false = False
true = True

# [Global_Variables]
# None

# [Code]
# [Imports]
from dataclasses import dataclass

# [Local Imports]
from helper import *

@dataclass
class Constants:
    ADD = Mode.ADD
    SUBTRACT = Mode.SUBTRACT
    INTERSECT = Mode.INTERSECT
    CENTER = Align.CENTER
    MIN = Align.MIN
    MAX = Align.MAX
    CCC = (Align.CENTER, Align.CENTER, Align.CENTER)
C = Constants()

# [Classes]
@dataclass
class Parameters:
    """Parameters for the ${TM_FILENAME}"""

    show_debug: bool = yes
    show_selection: bool = no
    do_imports: bool = no
    do_details: bool = no
    do_post_processing: bool = no
    do_export: bool = yes

    # Device dimensions
    body_height: float = 190.0
    body_radius: float = 65.0
    body_width: float = 140.0
    body_extrude: float = 5.0
    
    clamp: float = 52.0
    thicken: float = 25.0
    outer_radius: float = 80.0-2.0

# [End of File]
