# mesh_info_click.py

import logging
from pathlib import Path

import click  # https://click.palletsprojects.com/
import trimesh  # https://trimsh.org/
from rich.console import Console
from rich.table import Table
from rich import box

S_LOG_MSG_FORMAT = "%(asctime)s [%(levelname)-5s]  %(message)s"
logging.basicConfig(format=S_LOG_MSG_FORMAT, level=logging.INFO)
log = logging.getLogger(__name__)

console = Console()


def load_mesh(path: Path) -> trimesh.Trimesh:
    """
    Load a 3D mesh file using trimesh and return the mesh object.
    """
    log.debug("load_mesh(path=%s)", path)
    try:
        mesh = trimesh.load_mesh(str(path), force='mesh')
        return mesh
    except Exception as e:
        log.error("Failed to load mesh: %s", e)
        raise click.ClickException("Mesh loading failed")


def print_mesh_info(mesh: trimesh.Trimesh, path: Path) -> None:
    """
    Print geometric information of the mesh using Rich.
    """
    log.debug("print_mesh_info(mesh=<%s>, path=%s)", type(mesh), path)

    bbox = mesh.bounds
    size = mesh.extents
    volume = mesh.volume if mesh.is_watertight else "N/A"
    surface = mesh.area

    obb = mesh.bounding_box_oriented
    obb_size = obb.primitive.extents

    table = Table(title=f"Mesh Info: {path.name}", box=box.SIMPLE_HEAVY)
    table.add_column("Property", style="bold cyan")
    table.add_column("Value", style="bold white")

    table.add_row("Vertices", str(len(mesh.vertices)))
    table.add_row("Faces", str(len(mesh.faces)))
    table.add_row("Watertight", str(mesh.is_watertight))
    table.add_row("Surface Area", f"{surface:.2f} mm²")
    table.add_row("Volume", str(volume))
    table.add_row("Size (AABB)", f"{size[0]:.2f} x {size[1]:.2f} x {size[2]:.2f} mm")
    table.add_row("Size (OBB)", f"{obb_size[0]:.2f} x {obb_size[1]:.2f} x {obb_size[2]:.2f} mm")
    table.add_row("Bounding Box Min", str(bbox[0]))
    table.add_row("Bounding Box Max", str(bbox[1]))
    table.add_row("Center of Mass", str(mesh.center_mass))

    console.print(table)


@click.command()
@click.argument("file", type=click.Path(exists=True, path_type=Path))
def info(file: Path) -> None:
    """
    Load a 3D mesh and print its size and geometry info.
    """
    log.debug("info(file=%s)\n", file)
    mesh = load_mesh(file)
    print_mesh_info(mesh, file)
    log.info("So long, and thanks for all the mesh!")


if __name__ == "__main__":
    info()
