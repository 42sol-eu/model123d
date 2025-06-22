import math
import random

SVG_WIDTH = 800
SVG_HEIGHT = 400
NUM_LINES = 18
LINE_SPACING = SVG_HEIGHT // (NUM_LINES + 1)
NUM_DROPS = 5
DROP_MIN_RADIUS = 60
DROP_MAX_RADIUS = 120
DROP_HEIGHT = 100  # max vertical offset at center
STEP = 1  # horizontal step size for line drawing
PARABOLIC_POWER = 2.5  # Higher = more parabolic, sharper center, flatter edge
SMOOTHING_ITER = 18  # Number of smoothing iterations
SMOOTHING_STRENGTH = 0.38  # How much to nudge per iteration (0-1)
SINUS_FREQ = 0.012  # frequency of the slow sinus
SINUS_AMP = 7.0     # amplitude of the slow sinus


def generate_drops(num_drops=NUM_DROPS, min_radius=DROP_MIN_RADIUS, max_radius=DROP_MAX_RADIUS):
    drops = []
    attempts = 0
    while len(drops) < num_drops and attempts < 1000:
        r = random.randint(min_radius, max_radius)
        cx = random.randint(r + 20, SVG_WIDTH - r - 20)
        cy = random.randint(r + 20, SVG_HEIGHT - r - 20)
        # Ensure drops do not overlap
        overlap = False
        for (ocx, ocy, orad) in drops:
            if math.hypot(cx - ocx, cy - ocy) < r + orad + 12:
                overlap = True
                break
        if not overlap:
            drops.append((cx, cy, r))
        attempts += 1
    return drops


def drop_lens_bend(x, y0, cx, cy, r, strength=DROP_HEIGHT, power=PARABOLIC_POWER):
    """
    Returns the vertical offset for a point (x, y0) due to a lens at (cx, cy) with radius r.
    The bend is symmetric: above the center bends up, below bends down, max at center.
    The profile is more parabolic for higher power.
    """
    dx = x - cx
    dy = y0 - cy
    d = math.hypot(dx, dy)
    if d > r:
        return 0.0
    norm = d / r
    lens_profile = (1 - norm ** 2) ** power
    direction = math.copysign(1, dy) if dy != 0 else 0
    return direction * abs(dy) / r * lens_profile * strength


def simulate_lines_with_drops():
    drops = generate_drops()
    lines = []
    for i in range(NUM_LINES):
        if i % 2 == 0:
            print('.', end='', flush=True)  # progress indicator
        y0 = (i + 1) * LINE_SPACING
        # Each branch is a tuple: (list of points, set of split_drop_ids)
        branches = [([(0, y0)], set())]
        x = 0
        phase = random.uniform(0, 2 * math.pi)
        drop_centers = [(cx, cy, r) for (cx, cy, r) in drops]
        while x < SVG_WIDTH:
            new_branches = []
            for branch, split_drops in branches:
                last_x, last_y = branch[-1]
                next_x = last_x + STEP
                sinus_offset = math.sin(next_x * SINUS_FREQ + phase) * SINUS_AMP
                next_y = y0 + sinus_offset
                forbidden = False
                split_this_step = False
                for drop_id, (cx, cy, r) in enumerate(drop_centers):
                    d = math.hypot(next_x - cx, y0 - cy)
                    if d < 0.25 * r:
                        if drop_id not in split_drops:
                            forbidden = True
                            offset = 0.28 * r
                            dy = y0 - cy
                            direction = 1 if dy >= 0 else -1
                            above_y = cy - direction * offset + sinus_offset
                            below_y = cy + direction * offset + sinus_offset
                            # Mark this drop as split for both new branches
                            new_branches.append((branch + [(next_x, above_y)], split_drops | {drop_id}))
                            new_branches.append((branch + [(next_x, below_y)], split_drops | {drop_id}))
                            split_this_step = True
                        break
                if not forbidden and not split_this_step:
                    for cx, cy, r in drop_centers:
                        d = abs(next_x - cx)
                        if d < 1.1 * r:
                            next_y += drop_lens_bend(next_x, y0, cx, cy, r)
                    branch.append((next_x, next_y))
                    new_branches.append((branch, split_drops))
            if not new_branches:
                break  # all branches are stuck
            branches = new_branches
            x += STEP
        for branch, _ in branches:
            if branch[-1][0] >= SVG_WIDTH - STEP:
                lines.append(branch)
    print()  # newline after progress
    return lines, drops


def generate_svg(lines, drops, svg_path="drop_simulation.svg"):
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_WIDTH}" height="{SVG_HEIGHT}" viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}">',
    ]
    # Draw drops
    for cx, cy, r in drops:
        svg.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{r}" fill="#a2d2ff" stroke="#457b9d" stroke-width="2.5" opacity="0.45"/>')
    # Draw lines
    for points in lines:
        d = f'M {points[0][0]:.2f},{points[0][1]:.2f} '
        for x, y in points[1:]:
            d += f'L {x:.2f},{y:.2f} '
        svg.append(f'<path d="{d}" fill="none" stroke="#222" stroke-width="2.2" opacity="0.85"/>')
    svg.append('</svg>')
    with open(svg_path, "w") as f:
        f.write("\n".join(svg))
    print(f"SVG saved to {svg_path}")


def main():
    lines, drops = simulate_lines_with_drops()
    generate_svg(lines, drops)

if __name__ == "__main__":
    main()
