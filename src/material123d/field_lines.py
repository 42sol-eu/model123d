import math
import random

SVG_WIDTH = 800
SVG_HEIGHT = 400
BALL_COUNT = 50
BALL_SPEED = 4.0  # pixels per step
BALL_RADIUS = 2
STEPS = 400

CENTER_X = SVG_WIDTH // 2
CENTER_Y = SVG_HEIGHT // 2
LENS_RADIUS = 80
N_OUTSIDE = 1.0  # refractive index outside
N_INSIDE = 1.1   # refractive index inside (e.g., glass)


def snell_law(n1, n2, incident_angle):
    # Returns the refracted angle (in radians) or None if total internal reflection
    try:
        sin_theta2 = n1 / n2 * math.sin(incident_angle)
        if abs(sin_theta2) > 1:
            return None  # total internal reflection
        return math.asin(sin_theta2)
    except Exception:
        return None


def simulate_light_rays(ball_count=BALL_COUNT, speed=BALL_SPEED, steps=STEPS):
    """
    Simulate light rays from left to right, refracting through a circular region in the center.
    Returns a list of trajectories (list of (x, y) tuples for each ray).
    """
    trajectories = []
    for i in range(ball_count):
        y0 = int((i + 1) * SVG_HEIGHT / (ball_count + 1))
        x, y = 30, y0
        angle = 0.0  # horizontal
        n_current = N_OUTSIDE
        path = [(x, y)]
        for _ in range(steps):
            # Check if crossing lens boundary
            dist_to_center = math.hypot(x - CENTER_X, y - CENTER_Y)
            inside = dist_to_center < LENS_RADIUS
            # Compute next position
            x_next = x + speed * math.cos(angle)
            y_next = y + speed * math.sin(angle)
            dist_next = math.hypot(x_next - CENTER_X, y_next - CENTER_Y)
            crossed = (inside and dist_next >= LENS_RADIUS) or (not inside and dist_next < LENS_RADIUS)
            if crossed:
                # Find intersection point with circle boundary
                dx = math.cos(angle)
                dy = math.sin(angle)
                cx, cy = CENTER_X, CENTER_Y
                fx, fy = x - cx, y - cy
                a = dx * dx + dy * dy
                b = 2 * (fx * dx + fy * dy)
                c = fx * fx + fy * fy - LENS_RADIUS * LENS_RADIUS
                disc = b * b - 4 * a * c
                if disc < 0:
                    break  # no intersection
                t = (-b + (1 if inside else -1) * math.sqrt(disc)) / (2 * a)
                x_int = x + t * dx
                y_int = y + t * dy
                # Normal at intersection
                nx = (x_int - cx) / LENS_RADIUS
                ny = (y_int - cy) / LENS_RADIUS
                # Incident angle
                dot = dx * nx + dy * ny
                incident_angle = math.acos(dot)
                # Determine n1, n2
                n1 = N_INSIDE if inside else N_OUTSIDE
                n2 = N_OUTSIDE if inside else N_INSIDE
                # Refract
                refracted_angle = snell_law(n1, n2, incident_angle)
                if refracted_angle is None:
                    break  # total internal reflection
                # New direction: rotate tangent to normal by refracted_angle
                tangent_angle = math.atan2(ny, nx) + math.pi / 2
                if dot < 0:
                    new_angle = tangent_angle - refracted_angle
                else:
                    new_angle = tangent_angle + refracted_angle
                # Step to intersection, then continue
                x, y = x_int, y_int
                angle = new_angle
                n_current = n2
                path.append((x, y))
            else:
                x, y = x_next, y_next
                path.append((x, y))
            if not (0 <= x <= SVG_WIDTH and 0 <= y <= SVG_HEIGHT):
                break
        trajectories.append(path)
    return trajectories


def generate_svg(trajectories, svg_path="field_lines.svg"):
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_WIDTH}" height="{SVG_HEIGHT}" viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}">',
        f'<circle cx="{CENTER_X}" cy="{CENTER_Y}" r="{LENS_RADIUS}" fill="#e0e6f8" stroke="#457b9d" stroke-width="3" opacity="0.5"/>',
    ]
    colors = ["#e63946", "#457b9d", "#2a9d8f", "#f4a261", "#a8dadc", "#ffb703", "#b5838d", "#6d6875", "#264653", "#f3722c"]
    for i, path in enumerate(trajectories):
        color = colors[i % len(colors)]
        d = f'M {path[0][0]:.2f},{path[0][1]:.2f} '
        for x, y in path[1:]:
            d += f'L {x:.2f},{y:.2f} '
        svg.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="2.5" opacity="0.85"/>')
        bx, by = path[-1]
        svg.append(f'<circle cx="{bx:.2f}" cy="{by:.2f}" r="{BALL_RADIUS}" fill="{color}" stroke="#222" stroke-width="1.2"/>')
    svg.append('</svg>')
    with open(svg_path, "w") as f:
        f.write("\n".join(svg))
    print(f"SVG saved to {svg_path}")


def main():
    trajectories = simulate_light_rays()
    generate_svg(trajectories)

if __name__ == "__main__":
    main()
