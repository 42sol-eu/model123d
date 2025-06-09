from parameter import Parameters
from helper import debug, export_parts_to_stl
from phone_model import get_phone_objects
from phone_backplate import get_backplate_objects

def export_all(P: Parameters, file_name: str, objects: dict, console):
    """Export the model and its parts to STL/3MF files if P.do_export is True. Expects the same objects dict as used in show()."""
    if not P.do_export:
        return
    debug("Exporting model")
    id = f'1'
    export_name = file_name \
                    .replace('{identifier}', id) \
                    .replace('.py', '.stl')
    from pathlib import Path
    export_path = Path(file_name).parent / export_name
    console.log(f"[green]Model exported to {export_path}[/green]")

    # Helper to extract parts from the objects dict
    def get_part(obj, *keys):
        for key in keys:
            obj = obj[key]
        return obj

    # Full model (flatten all parts in objects dict)
    parts = []
    for section in objects.values():
        if isinstance(section, dict):
            for part in section.values():
                parts.append(part)
        else:
            parts.append(section)
    export_parts_to_stl(export_path, parts)

    # Individual parts (example: phone, backplate, etc.)
    if 'phone' in objects:
        phone = objects['phone']
        if 'body' in phone:
            export_parts_to_stl((export_path, "phone", "1"), [phone['body']])
        if 'display' in phone:
            export_parts_to_stl((export_path, "display", "1"), [phone['display']])
        if 'addons' in backplate:
            export_parts_to_stl([export_path, "addons", "1"], [backplate['charger']])
    elif 'backplate' in objects:
        backplate = objects['backplate']
        if 'backplate' in backplate:
            export_parts_to_stl((export_path, "backplate", "1"), [backplate['backplate']])
    elif 'belta' in objects:
        case = objects['belta']
        export_parts_to_stl((export_path, "belta", "1"), [case['case']])
    else:
        console.log("[red]No phone or backplate objects found to export.[/red]")

    # TODO: 3mf export
    # export_name = export_name.replace('.stl', '.3mf')
    # export_path = Path(__file__).parent / export_name

if __name__ == "__main__":
    from phone_model import build_phone_model
    from phone_addons import build_phone_addons
    from phone_backplate import build_phone_backplate
    from rich.console import Console
    P = Parameters()
    console = Console()
    display_cutout, display, phone, addons = build_phone_model(P)
    screws, backplate, charger, charger_frame = build_phone_backplate(P)
    
    objects = \
    {
            "phone": get_phone_objects(),
            "backplate": get_backplate_objects(),
            #"belta": {
            #    'case': case.part,
            #},
    }
    export_all(P, __file__, objects, console)
