from parameter import Parameters
from helper import debug, export_parts_to_stl

def export_all(P: Parameters, objects: dict, console):
    """Export the model and its parts to STL/3MF files if P.do_export is True. Expects the same objects dict as used in show()."""
    if not P.do_export:
        return
    debug("Exporting model")
    id = f'1'
    export_name = __file__ \
                    .replace('{identifier}', id) \
                    .replace('.py', '.stl')
    from pathlib import Path
    export_path = Path(__file__).parent / export_name
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
    if 'backplate' in objects:
        backplate = objects['backplate']
        if 'backplate' in backplate:
            export_parts_to_stl((export_path, "backplate", "1"), [backplate['backplate']])
        if 'charger' in backplate:
            export_parts_to_stl([export_path, "addons", "1"], [backplate['charger']])
    # Add more as needed for your structure

    # 3mf export
    export_name = export_name.replace('.stl', '.3mf')
    export_path = Path(__file__).parent / export_name

if __name__ == "__main__":
    from phone_model import build_phone_model
    from phone_addons import build_phone_addons
    from phone_backplate import build_phone_backplate
    from rich.console import Console
    P = Parameters()
    console = Console()
    display_cutout, display, phone = build_phone_model(P)[:3]
    addons = build_phone_addons(P)
    camera1, camera1_frame, camera1_lense, camera1_inner, camera1_outer, camera1_lense, camera1_back = addons['camera1']
    led, outer, inner = addons['led']
    camera2, camera2_frame, camera2_lense, camera2_inner, camera2_outer, camera2_lense, camera2_back = addons['camera2']
    camera3, camera3_frame, camera3_lense, camera3_inner, camera3_outer, camera3_lense, camera3_back = addons['camera3']
    _, backplate, charger, charger_frame = build_phone_backplate(P)
    export_all(P, display, phone, backplate, charger, camera1_frame, camera2_frame, camera3_frame, charger_frame, camera1_lense, camera2_lense, camera3_lense, console)
