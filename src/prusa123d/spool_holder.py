#TODO: add file header 

from pathlib import Path

from build123d import * # [docs](https://build123d.readthedocs.io/en/latest/)
from ocp_vscode import *


# TODO: create parameters 

class Parameters():
    def __init__(self):
        self.spool_diameter = 30
        self.spool_width = 10
        self.holder_height = 15
        self.holder_thickness = 5
        
# TODO: create Model 

class Model():
    def __init__(self, params):
        self.params = params
        
        importer = Mesher()
        self.path = Path(__file__).parent
        input_file = self.path / "mmu_enclosure_spoolholder_r3.stl"
        self.original_stl = importer.read(input_file)[0]

        
    def build(self):
        p = self.params
        
        with BuildPart() as part:
            with Locations(((0, 0, 20),)):
                spool = Cylinder(p.spool_diameter / 2, p.spool_width)
                holder = Cylinder((p.spool_diameter / 2) + p.holder_thickness, p.holder_height)
                holder = holder.cut(spool.translate((0, 0, (p.holder_height - p.spool_width) / 2)))
        return holder
    
m = Model(Parameters())
part = m.build()
show([part, m.original_stl.translate((0, 0, 0))])