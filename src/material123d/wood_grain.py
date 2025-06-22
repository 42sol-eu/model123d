import math  # https://docs.python.org/3/library/math.html
import logging  # https://docs.python.org/3/library/logging.html
from typing import Tuple
import random

import click  # https://click.palletsprojects.com/
from noise import pnoise2  # https://pypi.org/project/noise/
from PIL import Image  # https://pillow.readthedocs.io/en/stable/
from rich.console import Console  # https://rich.readthedocs.io/en/stable/

S_LOG_MSG_FORMAT = "%(asctime)s [%(levelname)-5s]  %(message)s"
logging.basicConfig(level=logging.INFO, format=S_LOG_MSG_FORMAT)
logger = logging.getLogger(__name__)
console = Console()

# Wood type parameters: (scale, ring_freq, noise_strength)
WOOD_TYPES: dict[str, Tuple[float, float, float]] = {
    "oak": (0.08, 0.15, 3.0),
    "pine": (0.1, 0.12, 4.0),
    "mahogany": (0.06, 0.2, 2.0),
    "walnut": (0.07, 0.17, 2.5),
}

def _generate_branch_circles(width, height, num_circles=3, min_radius=20, max_radius=60):
    """
    Generate random branch circle centers and radii.
    """
    circles = []
    for _ in range(num_circles):
        cx = random.randint(int(0.1 * width), int(0.9 * width))
        cy = random.randint(int(0.1 * height), int(0.9 * height))
        r = random.randint(min_radius, max_radius)
        circles.append((cx, cy, r))
    return circles

def generate_wood_grain(
    width: int,
    height: int,
    scale: float,
    ring_freq: float,
    noise_strength: float,
    branch_strength: float,
    branch_circles: int = 3
) -> Image.Image:
    """
    Generate a wood grain texture with horizontal lines that curve around branch circles.
    """
    logger.debug(
        "Generating wood grain: scale=%.2f, ring_freq=%.2f, noise_strength=%.2f, branch_strength=%.2f, branch_circles=%d",
        scale, ring_freq, noise_strength, branch_strength, branch_circles
    )

    image = Image.new("L", (width, height))
    pixels = image.load()

    # Generate branch circles (branch cross-sections)
    circles = _generate_branch_circles(width, height, num_circles=branch_circles)

    for y in range(height):
        for x in range(width):
            # Horizontal grain base
            base = x * ring_freq

            # Noise for texture
            noise_val = pnoise2(x * scale, y * scale, octaves=4)
            distortion = noise_val * noise_strength

            # Branch-like streaks
            branch_val = branch_strength * pnoise2(
                x * scale * 0.5,
                y * scale * 0.3,
                octaves=2
            )

            # Bend grain lines around branch circles
            bend = 0.0
            for cx, cy, r in circles:
                dx = x - cx
                dy = y - cy
                dist = math.sqrt(dx * dx + dy * dy)
                if dist < r * 1.5:
                    # Angle from center, used to curve the grain
                    angle = math.atan2(dy, dx)
                    # The closer to the circle, the more the grain is bent
                    bend += math.sin(angle) * (r * 1.5 - dist) / (r * 1.5) * 2.5
            
            # Final grain pattern: horizontal lines, bent by branches, with noise
            grain_value = 128 + 127 * math.sin(base + distortion + branch_val * 5.0 + bend)

            # Clamp and write pixel
            value = int(max(0, min(255, grain_value)))
            pixels[x, y] = value

    logger.debug("Wood grain generation complete.")
    return image

def generate_wood_grain_svg(
    width: int = 512,
    height: int = 512,
    num_lines: int = 40,
    waviness: float = 20.0,
    branch_circles: int = 3,
    min_radius: int = 20,
    max_radius: int = 50,
    svg_path: str = "wood_grain.svg"
):
    """
    Generate a wood grain SVG with wavy grain lines and branch circles.
    """
    import random
    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#f5e6c8"/>'
    ]

    # Generate branch circles
    circles = []
    for _ in range(branch_circles):
        cx = random.randint(int(0.15 * width), int(0.85 * width))
        cy = random.randint(int(0.15 * height), int(0.85 * height))
        r = random.randint(min_radius, max_radius)
        circles.append((cx, cy, r))
        svg_lines.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#b48a5a" stroke-width="2" opacity="0.7"/>')

    # Generate grain lines
    for i in range(num_lines):
        y = int(height * (i + 1) / (num_lines + 1))
        path = f'M 0 {y} '
        x = 0
        while x < width:
            # Waviness, modulated by proximity to branch circles
            wave = waviness * (0.5 + random.random())
            bend = 0.0
            for cx, cy, r in circles:
                dist = math.hypot(x - cx, y - cy)
                if dist < r * 1.5:
                    angle = math.atan2(y - cy, x - cx)
                    bend += math.sin(angle) * (r * 1.5 - dist) / (r * 1.5) * waviness * 1.5
            y_offset = math.sin(x / 60.0 + i) * wave + bend
            path += f'Q {x + 15} {y + y_offset:.2f}, {x + 30} {y + y_offset:.2f} '
            x += 30
        svg_lines.append(f'<path d="{path}" fill="none" stroke="#b48a5a" stroke-width="2" opacity="0.8"/>')

    svg_lines.append('</svg>')
    with open(svg_path, "w") as f:
        f.write("\n".join(svg_lines))
    logger.info(f"Wood grain SVG saved to {svg_path}")


def _generate_non_overlapping_knots(width, height, num_knots, min_radius, max_radius, max_attempts=1000):
    import random
    knots = []
    attempts = 0
    while len(knots) < num_knots and attempts < max_attempts:
        rx = random.randint(min_radius, max_radius)
        ry = int(rx * (0.7 + 0.6 * random.random()))  # ellipse
        cx = random.randint(rx + 10, width - rx - 10)
        cy = random.randint(ry + 10, height - ry - 10)
        overlap = False
        for (ocx, ocy, orx, ory) in knots:
            dx = cx - ocx
            dy = cy - ocy
            # Use ellipse bounding box for overlap check
            if (abs(dx) < rx + orx + 6) and (abs(dy) < ry + ory + 6):
                overlap = True
                break
        if not overlap:
            knots.append((cx, cy, rx, ry))
        attempts += 1
    return knots

def generate_wood_board_with_knots_svg(
    width: int = 800,
    height: int = 250,
    num_knots: int = 5,
    min_radius: int = 10,
    max_radius: int = 18,
    num_rings: int = 14,
    ring_bend_strength: float = 1.2,
    svg_path: str = "wood_board_knots.svg"
):
    """
    Generate an SVG of a wood board with non-overlapping ellipses for knots and trunk lines that bend smoothly around them, with bending based on distance to knot center and no bend beyond 3x radius.
    """
    import random, math
    def smoothstep(x):
        return 3 * x ** 2 - 2 * x ** 3
    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        f'<rect x="0" y="0" width="{width}" height="{height}" fill="#f5e6c8" stroke="#b48a5a" stroke-width="6"/>'
    ]
    knots = _generate_non_overlapping_knots(width, height, num_knots, min_radius, max_radius)
    for cx, cy, rx, ry in knots:
        svg_lines.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#b48a5a" stroke="#7a5832" stroke-width="2" opacity="0.85"/>')
    for i in range(num_rings):
        y_base = int(height * (i + 1) / (num_rings + 1))
        points = []
        x = 0
        step = 2
        thickness = 0.7 + 1.2 * random.random()
        while x < width:
            y = y_base
            bend = 0.0
            for cx, cy, rx, ry in knots:
                r = (rx + ry) / 2
                dx = x - cx
                dy = y_base - cy
                dist = math.hypot(dx, dy)
                if dist < 3 * r:
                    # Normalized: 0 at center, 1 at 3*r
                    t = min(max((dist - r) / (2 * r), 0.0), 1.0)
                    # Use a smoothstep for a gentle transition
                    influence = 1.0 - smoothstep(t)
                    # Direction: up or down depending on y_base vs cy
                    sign = 1 if y_base < cy else -1
                    # Bend peaks at the edge of the knot, fades to zero at 3*r
                    if dist > r:
                        bend += sign * influence * ring_bend_strength * r * 0.7
                    else:
                        # Inside the knot: don't draw
                        bend = None
                        break
            if bend is not None:
                y += bend
                points.append((x, y))
            x += step
        if points:
            d = f'M {points[0][0]:.2f},{points[0][1]:.2f} '
            for px, py in points[1:]:
                d += f'L {px:.2f},{py:.2f} '
            svg_lines.append(f'<path d="{d}" fill="none" stroke="#b48a5a" stroke-width="{thickness:.2f}" opacity="0.7"/>')
    svg_lines.append('</svg>')
    with open(svg_path, "w") as f:
        f.write("\n".join(svg_lines))
    logger.info(f"Wood board SVG with knots and year rings saved to {svg_path}")

@click.command()
@click.option(  "--type", "-t", "wood_type", type=click.Choice(WOOD_TYPES.keys(), case_sensitive=False),
                default="walnut", help="Type of wood grain to generate")
@click.option(  "--width", "-w", default=512, show_default=True, help="Image width in pixels", type=int)
@click.option(  "--height", "-h", default=512, show_default=True, help="Image height in pixels", type=int)
@click.option(  "--branch", "-b", default=0.5, show_default=True,
                help="Branch swirl strength (0.0 = none, try 0.5 to 2.0)", type=float)
@click.option(  "--branch-circles", "-c", default=2, show_default=True,
                help="Number of branch circles (cross-sections) to add", type=int)
@click.option(  "--save", "-s", type=click.Path(dir_okay=False, writable=True), help="Path to save image")
def main(wood_type: str, width: int, height: int, branch: float, branch_circles: int, save: str | None) -> None:
    """
    Generate and show a wood grain image with optional branch swirls and branch circles.
    """
    try:
        wood_type = wood_type.lower()
        scale, ring_freq, noise_strength = WOOD_TYPES[wood_type]
        logger.info("Selected wood type: %s", wood_type)

        img = generate_wood_grain(width, height, scale, ring_freq, noise_strength, branch, branch_circles)

        if save:
            img.save(save)
            console.print(f"[green]Wood grain image saved to:[/green] {save}")
        else:
            img.show()

    except Exception as e:
        logger.exception("An error occurred during generation: %s", e)
    finally:
        logger.info("So long, and thanks for all the branches.")

@click.command("svg")
@click.option("--width", default=512, show_default=True, help="SVG width in pixels", type=int)
@click.option("--height", default=512, show_default=True, help="SVG height in pixels", type=int)
@click.option("--lines", default=40, show_default=True, help="Number of grain lines", type=int)
@click.option("--waviness", default=20.0, show_default=True, help="Waviness of grain lines", type=float)
@click.option("--branch-circles", default=3, show_default=True, help="Number of branch circles", type=int)
@click.option("--output", default="wood_grain.svg", show_default=True, help="Output SVG file path", type=str)
def svg(width, height, lines, waviness, branch_circles, output):
    """
    Generate a wood grain SVG with wavy lines and branch circles.
    """
    generate_wood_grain_svg(width, height, lines, waviness, branch_circles, svg_path=output)
    console.print(f"[green]Wood grain SVG saved to:[/green] {output}")

@click.command("board-svg")
@click.option("--width", default=800, show_default=True, help="SVG width in pixels", type=int)
@click.option("--height", default=250, show_default=True, help="SVG height in pixels", type=int)
@click.option("--knots", default=5, show_default=True, help="Number of branch holes (knots)", type=int)
@click.option("--output", default="wood_board_knots.svg", show_default=True, help="Output SVG file path", type=str)
def board_svg(width, height, knots, output):
    """
    Generate a wood board SVG with 3-10 irregular branch holes (knots).
    """
    generate_wood_board_with_knots_svg(width, height, knots, svg_path=output)
    console.print(f"[green]Wood board SVG with knots saved to:[/green] {output}")

@click.group()
def cli():
    """Wood grain generator CLI."""
    pass

cli.add_command(main, name="main")
cli.add_command(svg)
cli.add_command(board_svg)

if __name__ == "__main__":
    cli()