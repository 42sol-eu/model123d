# [Imports]
from build123d import * 

# [Local Imports]
from parameter import Parameters
from helper import define

class Camera:
    def __init__(self,x, y, z, diameter, frame, height, name="camera"):
        """Initialize a camera object with its parameters"""
        self.create(x, y, z, diameter, frame, height, name)
    
    def create(self, x, y, z, diameter, frame, height, name="camera"):
        """Create a camera with a frame"""
        
        self.name = name
        self.x = x
        self.y = y
        self.z = z
        
        outer_radius = diameter / 2
        inner_radius = (diameter - frame) / 2
        
        with BuildPart(Plane.XY.offset(z)) as bottom:
            with Locations((x, y)):
                Cylinder(inner_radius, 0.01, mode=Mode.ADD)
                
        with BuildPart(Plane.XY.offset(z+0.01)) as outer:
            with Locations((x, y)):
                Cylinder(inner_radius*0.4, 0.01, mode=Mode.ADD)
                
        with BuildPart(Plane.XY.offset(z+0.02)) as inner:
            with Locations((x, y)):
                Cylinder(inner_radius*0.3, 0.01, mode=Mode.ADD)
                
        with BuildPart(Plane.XY.offset(z)) as frame:
            with BuildSketch(Plane.XY.offset(z)) as frame_sketch:
                with Locations((x, y)):
                    Circle(outer_radius, mode=Mode.ADD)
                    Circle(inner_radius, mode=Mode.SUBTRACT)
            extrude(amount=height, mode=Mode.ADD)
            
        with BuildPart(Plane.XY.offset(z+height/2)) as lense:
            with Locations((x, y)):
                Cylinder(inner_radius, height-0.05, mode=Mode.ADD)
        
        self.bottom = bottom
        define (bottom, "#000000ff", f'{name}_bottom')
        
        self.outer = outer
        define (outer, "#444343bb", f'{name}_outer')
        
        self.inner = inner
        define (inner, "#282877ff", f'{name}_inner')
        
        self.frame = frame
        define (frame,  "#bbbdbbff", f'{name}_frame')
        
        self.lense = lense
        define (lense,  "#f4f44b2c", f'{name}_lens', alpha=0.2)
        
        self.compound = Compound([frame.part, bottom.part, outer.part, inner.part, lense.part], label=name)
        define(self.compound, name=f'{name}')
        
        return self

    def to_dict(self):
        return {
            "frame": self.frame,
            "lense": self.lense,
            "inner": self.inner,
            "outer": self.outer,
            "bottom": self.bottom
        }
        
class Led:
    def __init__(self, x, y, z, diameter, name="led"):
        self.create(x, y, z, diameter, name)

    def create(self, x, y, z, diameter, name="led"):
        with BuildPart(Plane.XY.offset(z+0.01)) as outer:
            with Locations((x, y)):
                Cylinder(diameter, 0.01, mode=Mode.ADD)
        with BuildPart(Plane.XY.offset(z+0.02)) as inner:
            with Locations((x, y)):
                Cylinder(diameter*0.5, 0.01, mode=Mode.ADD)
                
        self.outer = outer 
        define(outer,  "#bbbdbbff", f'{name}_outer')
        
        self.inner = inner
        define(inner,  "#f4f44b2c", f'{name}_inner')
        led = Compound([outer.part, inner.part], label=name)
        
        self.led = led
        define(led, "#f4f44b2c", f'{name}_led')
        
        return self

    def to_dict(self):
        return {
            "outer": self.outer,
            "inner": self.inner
        }   
# [Code]

camera1 = None
camera2 = None
camera3 = None
led = None



def build_phone_addons(P: Parameters):
    """Builds the 3 cameras and the led, returns a dict with all parts"""
    global camera1, camera2, camera3, led
    
    camera1 = Camera(P.camera1_x, P.camera1_y+P.camera1_h/4, P.body_extrude, P.camera1_r*2-0.1, P.camera1_frame, P.camera1_extrude, 'camera1')
    camera2 = Camera(P.camera2_x, P.camera2_y, P.body_extrude, P.camera3_diameter-0.1, P.camera2_frame, P.camera2_extrude, 'camera2')
    camera3 = Camera(P.camera3_x, P.camera3_y, P.body_extrude, P.camera3_diameter-0.1, P.camera3_frame, P.camera3_extrude, 'camera3')
    led = Led(P.camera1_x, P.camera1_y-P.camera1_h/4, P.body_extrude, P.camera1_r*0.6, 'led')
    
    return camera1, camera2, camera3, led
    
    
def get_addon_objects():
    """Returns a dictionary of all addon objects"""
    return {
        'camera1': camera1.to_dict(),
        'camera2': camera2.to_dict(),
        'camera3': camera3.to_dict(),
        'led': led.to_dict()
    }

if __name__ == "__main__":
    P = Parameters()
    build_phone_addons(P)
    
    # Optionally show the model (if ocp_vscode/show is available)
    try:
        from ocp_vscode import show
        
        objects = {
            "addons": get_addon_objects()
        }
        show(objects)
        
    except ImportError:
        print("ocp_vscode not available, skipping show.")