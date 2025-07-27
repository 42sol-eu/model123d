from rich import print
import lib3mf                   # https://lib3mf.readthedocs.io/en/release-2.4.1/
from lib3mf import get_wrapper
import os
import trimesh

# Get version
def get_version(wrapper):
    major, minor, micro = wrapper.GetLibraryVersion()
    print("Lib3MF version: {:d}.{:d}.{:d}".format(major, minor, micro), end="")
    hasInfo, pre_release_info = wrapper.GetPrereleaseInformation()
    if hasInfo:
        print("-" + pre_release_info, end="")
    hasInfo, build_info = wrapper.GetBuildInformation()
    if hasInfo:
        print("+" + build_info, end="")
    print("")


# Create vertex in a mesh
def create_vertex(_mesh, x, y, z):
    position = lib3mf.Position()
    position.Coordinates[0] = float(x)
    position.Coordinates[1] = float(y)
    position.Coordinates[2] = float(z)
    _mesh.AddVertex(position)
    return position


# Add triangle in a mesh
def add_triangle(_mesh, p1, p2, p3):
    triangle = lib3mf.Triangle()
    triangle.Indices[0] = p1
    triangle.Indices[1] = p2
    triangle.Indices[2] = p3
    _mesh.AddTriangle(triangle)
    return triangle


# Create a transform matrix for positioning objects
def create_transform(wrapper, x_offset, y_offset, z_offset=0):
    # Create a proper transformation matrix
    # lib3mf expects a 4x4 transformation matrix as a flat array of 16 floats
    # in column-major order: m00, m10, m20, m30, m01, m11, m21, m31, m02, m12, m22, m32, m03, m13, m23, m33
    
    transform_array = [
        1.0, 0.0, 0.0, 0.0,  # Column 0: [1, 0, 0, 0]
        0.0, 1.0, 0.0, 0.0,  # Column 1: [0, 1, 0, 0]  
        0.0, 0.0, 1.0, 0.0,  # Column 2: [0, 0, 1, 0]
        float(x_offset), float(y_offset), float(z_offset), 1.0  # Column 3: [x, y, z, 1]
    ]
    
    # Create transform using the wrapper
    try:
        # Try to create transform from array
        transform = wrapper.CreateTransform(transform_array)
        return transform
    except Exception as e:
        print(f"CreateTransform error: {e}")
        # Fall back to identity transform
        return wrapper.GetIdentityTransform()


# Load STL file into a mesh object using trimesh with translation
def load_stl_file(model, stl_path, object_name, x_offset=0, y_offset=0, z_offset=0):
    if not os.path.exists(stl_path):
        print(f"STL file not found: {stl_path}")
        return create_simple_cube(model, object_name)
    
    try:
        # Load STL file using trimesh
        mesh = trimesh.load_mesh(stl_path)
        
        # ensure that the STL file has the object at the origin coordinates, fix it if not 
        centroid = mesh.centroid
        mesh.apply_translation(-centroid)

        if 0:
            print(f"Translated STL {stl_path} to origin (centroid: {centroid})")
        
        
        # Apply translation to the mesh if offsets are provided
        if x_offset != 0 or y_offset != 0 or z_offset != 0:
            import numpy as np
            translation_matrix = np.eye(4)
            translation_matrix[0, 3] = x_offset
            translation_matrix[1, 3] = y_offset
            translation_matrix[2, 3] = z_offset
            mesh.apply_transform(translation_matrix)
        
        # Create a mesh object for lib3mf
        mesh_object = model.AddMeshObject()
        mesh_object.SetName(object_name)
        
        # Add vertices from trimesh to lib3mf
        for vertex in mesh.vertices:
            create_vertex(mesh_object, float(vertex[0]), float(vertex[1]), float(vertex[2]))
        
        # Add triangles from trimesh to lib3mf
        for face in mesh.faces:
            add_triangle(mesh_object, int(face[0]), int(face[1]), int(face[2]))
        
        print(f"Loaded STL with {len(mesh.vertices)} vertices and {len(mesh.faces)} triangles at offset ({x_offset}, {y_offset}, {z_offset})")
        return mesh_object
    
    except Exception as e:
        print(f"Error loading STL file {stl_path}: {e}")
        print("Falling back to simple cube...")
        # Return a simple cube as fallback
        return create_simple_cube(model, object_name)


def create_simple_cube(model, object_name):
    """Create a simple cube as fallback when STL loading fails"""
    mesh_object = model.AddMeshObject()
    mesh_object.SetName(object_name)
    
    # Define the size of the cube
    fSizeX, fSizeY, fSizeZ = 1.0, 1.0, 1.0
    
    # Create vertices for a simple cube
    create_vertex(mesh_object, 0, 0, 0)
    create_vertex(mesh_object, fSizeX, 0, 0)
    create_vertex(mesh_object, fSizeX, fSizeY, 0)
    create_vertex(mesh_object, 0, fSizeY, 0)
    create_vertex(mesh_object, 0, 0, fSizeZ)
    create_vertex(mesh_object, fSizeX, 0, fSizeZ)
    create_vertex(mesh_object, fSizeX, fSizeY, fSizeZ)
    create_vertex(mesh_object, 0, fSizeY, fSizeZ)
    
    # Define triangles by vertices indices
    triangle_indices = [
        (2, 1, 0), (0, 3, 2), (4, 5, 6), (6, 7, 4),
        (0, 1, 5), (5, 4, 0), (2, 3, 7), (7, 6, 2),
        (1, 2, 6), (6, 5, 1), (3, 0, 4), (4, 7, 3)
    ]
    
    # Create triangles
    for v0, v1, v2 in triangle_indices:
        add_triangle(mesh_object, v0, v1, v2)
    
    return mesh_object



class Plate:
    def __init__(self, name, width, height ):
        self.name = name
        self.width = width
        self.height = height
        self.occupied = []
        self._row = 1
        self._column = 1
        self._active_x = 0.0
        self._active_y = 0.0
        self._active_height = 0.0
        self._active_width = 0.0
        self._max_width = 0.0
        self._max_height = 0.0
        self.set_spacing(10.0, 10.0)

        self._wrapper = get_wrapper()
        get_version(self._wrapper)
        self._model = self._wrapper.CreateModel()


    def set_spacing(self, spacing_x, spacing_y):
        """Set the spacing between objects."""
        self._spacing_x = spacing_x
        self._spacing_y = spacing_y
        print(f"Spacing set to: {self._spacing_x} (X), {self._spacing_y} (Y)")
        # self._active_x = self._spacing_x
        # self._active_y = self._spacing_y
    
    def add_object(self, x, y, obj_width, obj_height):
        """Add an object's bounding box to the plate."""
        bbox = (x, y, x + obj_width, y + obj_height)
        self.occupied.append(bbox)
        
    def update(self, x, y, width, height):
        """Update the active position on the plate."""
        self._active_x = x
        self._active_y = y
        self._max_height = max(self._max_height, height)
        self._max_width = max(self._max_width, width)

        if 1:
            print(f"Active position updated to: ({self._active_x}, {self._active_y}) max: ({self._max_width}, {self._max_height})")



    def check_space_in_row(self):
        """Check if there is space in the current row."""
        if self._active_y + self._spacing_y > self.height:
            return False
        return True
    
    def check_space_in_column(self) -> bool:
        """Check if there is space in the current column."""

        print(f'\n>>> Checking space at {self._row, self._column}: active_x={self._active_x}, spacing_x={self._spacing_x}, width={self.width}\n')

        if self._active_x + self._active_width + self._spacing_x > self.width:
            return False
        return True

    @property
    def row(self):
        return self._row 

    @property
    def column(self):
        return self._column    

    def next_row(self):
        self._column = 1
        self._active_x = self._spacing_x
        self._max_width = self._spacing_x
        self._row += 1
        self._active_y += self._max_height
        self._max_height = self._spacing_y

    def next_column(self):
        """Move to the next column."""
        self._column += 1
        self._active_x += self._spacing_x

class ObjectPlacer:
    def __init__(self, plate, spacing_x=10.0, spacing_y=10.0):
        self._plate = plate
        self._spacing_x = spacing_x
        self._spacing_y = spacing_y
        self._placed_objects = []
        self.stl_path = None
        self.num_objects = 0

    def load_model(self, model_file: str, move_to_origin=True):
        """Load the model from a file.
        This method loads an STL file and applies a translation to ensure the object is at the origin.
        
        Args:
            model_name (str): The name of the model.
            model_file (str): The path to the STL file.
            move_to_origin (bool): Whether to move the object to the origin coordinates.
        """
        self.stl_path = model_file
        self._name = os.path.splitext(os.path.basename(model_file))[0]
        self._mesh = trimesh.load_mesh(model_file)
        print(f"Model loaded from: {model_file}")

        if move_to_origin:  # ensure that the STL file has the object at the origin coordinates, fix it if not
            centroid = self._mesh.centroid
            self._mesh.apply_translation(-centroid)
            if 0:
                print(f"Translated model to origin (centroid: {centroid})")

        return self._mesh

    def place_object(self, row, col):
        """Place a single object at the specified row and column."""
        if row < 1 or col < 1:
            raise ValueError("Row and column must be positive integers starting from 1.")
        
        # Convert to 0-based indexing for calculations
        size_x, size_y, size_z = self._mesh.extents
        x = self._plate._active_x + size_x + self._spacing_x
        y = self._plate._active_y
        
        self._plate.update(x, y, size_x, size_y) 
        
        object_name = f"Object_{self.name}_{row}_{col}"

        if self._mesh:
            # Create a copy of the mesh for positioning
            positioned_mesh = self._mesh.copy()
            
            # Apply translation to position the mesh
            import numpy as np
            translation_matrix = np.eye(4)
            translation_matrix[0, 3] = x
            translation_matrix[1, 3] = y
            translation_matrix[2, 3] = 0
            positioned_mesh.apply_transform(translation_matrix)
            
            # Convert trimesh to lib3mf mesh object
            mesh_object = self._plate._model.AddMeshObject()
            mesh_object.SetName(object_name)
            
            # Add vertices from trimesh to lib3mf
            for vertex in positioned_mesh.vertices:
                create_vertex(mesh_object, float(vertex[0]), float(vertex[1]), float(vertex[2]))
            
            # Add triangles from trimesh to lib3mf
            for face in positioned_mesh.faces:
                add_triangle(mesh_object, int(face[0]), int(face[1]), int(face[2]))
            
            # Add build item with identity transform (mesh is already positioned)
            transform = self._plate._wrapper.GetIdentityTransform()
            self._plate._model.AddBuildItem(mesh_object, transform)
            self._placed_objects.append((object_name, (x, y, 0)))
            
            print(f"Added {object_name} at position ({x}, {y})")

    @property
    def name(self):
        return self._name
    
    @property
    def all_objects(self) -> int:
        return self.num_objects
    
    @property
    def to_place_objects(self) -> int:
        return self.num_objects - len(self._placed_objects)
    

    @property
    def placed_objects(self) -> int:
        return len(self._placed_objects)

    @property
    def spacing_x(self) -> float:
        return self._spacing_x

    @property
    def spacing_y(self) -> float:
        return self._spacing_y

    @property
    def stl_file_path(self) -> str:
        return self.stl_path
    
    def add(self, stl_path, num_objects):
        """Add a new STL file and number of objects to place."""
        self.stl_path = stl_path
        self.num_objects = num_objects        
        self._model = self.load_model(model_file=stl_path, move_to_origin=True)
        
        plate = self._plate
        print(f"add {num_objects} objects from {stl_path} to plate {plate.name}.")
        x,y,z = self._model.extents
        if 0:
            print(f"Model size: {x,y,z} ")
        # Create grid of objects
        for element in range(1, self.num_objects + 1):
            self.place_object(plate.row, plate.column)

            # Check if we need to move to next row 
            if not plate.check_space_in_column():
                plate.next_row()
            else:
                plate.next_column()
                



mk4plate = Plate("Mk4", width=220.0, height=220.0)
mk4plate.set_spacing(5.0, 5.0)

from pathlib import Path

placer = ObjectPlacer(plate=mk4plate)
placer.add(stl_path=str(Path(__file__).parent / "multiverse/box_end_cap_L.stl"), num_objects=4)
mk4plate.next_row()
placer.add(stl_path=str(Path(__file__).parent / "multiverse/box_corner_3.stl"),  num_objects=4)
mk4plate.next_row()
placer.add(stl_path=str(Path(__file__).parent / "multiverse/box_end_cap_I.stl"), num_objects=4)




# Save the model to a 3MF file
writer = mk4plate._model.QueryWriter("3mf")
output_file = "grid_2_4x3.3mf"
writer.WriteToFile(output_file)
print(f"Grid saved to {output_file}")