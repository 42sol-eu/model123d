# %%

from ocp_vscode import *
from build123d import *
from pathlib import Path

set_defaults(show_parent=False)

# %%

with BuildPart() as b:
    importer = Mesher()
    a = importer.read(Path(__file__).parent / "../src/material123d/wood/_output/wood_plank_200x200x1.2.stl")
    print(f'\n\n\n====\n{type(a)}\n======\n\n\n')
    #    add(shells.make_solid())
    with Locations((0, 2, 0)):
        Box(2, 2, 1)

push_object(b.solids(), name="green", color="green", alpha=0.7, clear=True)

# %%
show_objects()

# %%