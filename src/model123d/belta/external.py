# [Imports]
from build123d import *
from pathlib import Path

# [Local Imports]
from helper import *

# [Code]

def load_backplate_original():
    debug("Loading backplate")
    # Import an STL part (replace with your STL file path)
    stl_path = Path(__file__).parent / "_import"  / "cmf_phone_2_pro_universal_cover_2.stl"
    try:
        backplate = import_stl(stl_path)
        backplate.move(loc=Location((-P.body_width-8,-23.35,P.body_extrude-0.8)))
        # .rotate(Axis.Z, 45)  # Rotate the backplate to match the orientation
        define(backplate, "#ffffffdd", "backplate_imported")
        debug(f"Imported STL part from {stl_path}. {type(backplate)}")
    
    except Exception as e:
        debug(f"Failed to import STL: {e}")
    
    return backplate

def load_imports():
    objects = {}
    import_backplate = load_backplate_original()
    objects['original_backplate'] = import_backplate
    
    return objects

if __name__ == "__main__":
    from ocp_vscode import show
    
    objects = load_imports()
    show(objects, glass=yes)