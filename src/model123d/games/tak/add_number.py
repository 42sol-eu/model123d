import os
import zipfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import io

# Paths
base_dir = Path(__file__).parent
mf3_path = base_dir / '_export/14a__tak_field_4x4_magnets.3mf'  # Path to the 3MF file

# Open the 3MF file and extract thumbnail
with zipfile.ZipFile(mf3_path, 'r') as zip_file:
    # Read the thumbnail from the 3MF file
    thumbnail_data = zip_file.read('Metadata/thumbnail.png')
    img = Image.open(io.BytesIO(thumbnail_data)).convert("RGBA")

# Create overlay
overlay = Image.new("RGBA", img.size, (255,255,255,0))
draw = ImageDraw.Draw(overlay)

# Font settings (128 pts)
font_size = 128
font = None

# Try to find a system font on macOS
font_paths = [
    "/System/Library/Fonts/Arial.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    "/Library/Fonts/Arial.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",  # Linux fallback
    "arial.ttf"  # Windows fallback
]

for font_path in font_paths:
    try:
        font = ImageFont.truetype(font_path, font_size)
        print(f"Using font: {font_path}")
        break
    except (IOError, OSError):
        continue

# If no TrueType font found, use default and warn user
if font is None:
    print("Warning: No scalable font found. Text will be very small.")
    print("Consider installing a TrueType font or using a different approach.")
    font = ImageFont.load_default()

# Text settings
text = "14a"
bbox = draw.textbbox((0, 0), text, font=font)
text_width = bbox[2] - bbox[0]
text_height = bbox[3] - bbox[1]
x = (img.size[0] - text_width) // 2
y = (img.size[1] - text_height) // 2

# Draw text (white with black outline)
draw.text((x-2, y-2), text, font=font, fill="black")
draw.text((x+2, y-2), text, font=font, fill="black")
draw.text((x-2, y+2), text, font=font, fill="black")
draw.text((x+2, y+2), text, font=font, fill="black")
draw.text((x, y), text, font=font, fill="white")

# Composite overlay
result = Image.alpha_composite(img, overlay)

# Save the modified image back to the 3MF file
with io.BytesIO() as output_buffer:
    result.save(output_buffer, format='PNG')
    modified_thumbnail_data = output_buffer.getvalue()

# Update the 3MF file with the modified thumbnail
with zipfile.ZipFile(mf3_path, 'a') as zip_file:
    # Remove the old thumbnail
    # Note: zipfile doesn't support direct deletion, so we create a new file
    pass

# Create a new 3MF file with the modified thumbnail
temp_path = mf3_path.with_suffix('.tmp')
with zipfile.ZipFile(mf3_path, 'r') as old_zip:
    with zipfile.ZipFile(temp_path, 'w') as new_zip:
        for item in old_zip.infolist():
            if item.filename == 'Metadata/thumbnail.png':
                # Replace with modified thumbnail
                new_zip.writestr(item.filename, modified_thumbnail_data)
            else:
                # Copy other files unchanged
                new_zip.writestr(item.filename, old_zip.read(item.filename))

# Replace the original file
temp_path.replace(mf3_path)
print(f"Successfully updated thumbnail in {mf3_path}")
