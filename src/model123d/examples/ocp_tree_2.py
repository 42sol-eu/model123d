from build123d import *
from ocp_vscode import show_object

objects = {}

def define(object, color="#ff0000", name="", parent=None):
    """Define an object with a name and color"""
    if parent is not None:
        parent = objects 
    
    if type(object) is list or type(object) is tuple:
        objects[name] = {}
        for item in object:
            define(item, color=color, name=name, parent=objects[name])
        
    elif type(object) is dict:
        objects[name] = {}
        for k, v in object.items():
            define(v, color=color, name=k, parent=objects[name])
        
    elif type(object) is str or type(object) is int or type(object) is float:
        objects[str(object)] = {}
        
    else:    
        if len(name) == 0:
            if hasattr(object, '__name__'):
                name = object.__name__
            else:
                name = [k for k, v in globals().items() if v is object and not k.startswith("__")]
                name = name[0] if name else "unnamed"
        
        if '.' in name:
            is_top_level = False
            names = name.split('.')[-1]
            active_parent = objects
            for element in names:
                pass
                    

        object.name = name
        object.color = color
        
        if type(parent) is list:
            objects.append(object)
        elif type(parent) is dict:
            parent[name] = object
        

with BuildPart() as p:
    Box(0.1, 0.1, 2)

a = {
    "a": Vector(1, 2, 3),
    "b": [
        Pos(2, 2, 2) * Cylinder(1, 1),
        (1, 2, 3),
        p,
        p.part,
        {"c": Vector(5, 2, 3), "d": Pos(-3, 0, 0) * Box(1, 2, 3), "e": 123},
    ],
}
x = 0
b = [
    Pos(2, 4, 2) * Sphere(1),
    "wert",
    p,
    p.part,
    {"x": Pos(-5, -5, 0) * Box(2, 1, 0.5), "y": 123},
]

show_object(
    [a,p,b], name="green", options={"color": "green", "alpha": 0.2}, clear=True
)
