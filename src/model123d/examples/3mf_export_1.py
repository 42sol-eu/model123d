from build123d import *
from ocp_vscode import show


# Create parts with color
box = Box(10, 10, 10)
box.color = Color(1, 0, 0)

cyl = Cylinder(5, 10).move((15, 0, 0))
cyl.color = Color(0, 1, 0)

# Combine
combined = Compound([box, cyl])

# Show in ocp_vscode
show(combined)

# Export as 3MF
combined.export_3mf("colored_model.3mf")
