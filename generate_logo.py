from PIL import Image, ImageDraw, ImageFont
import os

# Ensure static/images directory exists
os.makedirs('static/images', exist_ok=True)

# Create a new image with white background
width, height = 200, 200
image = Image.new('RGBA', (width, height), (255, 255, 255, 0))
draw = ImageDraw.Draw(image)

# Draw outer circle with gradient (approximated with solid color)
draw.ellipse((10, 10, 190, 190), fill=(108, 99, 255))

# Draw inner circle with slightly different color
draw.ellipse((25, 25, 175, 175), fill=(78, 73, 208))

# Draw globe-like lines
center_x, center_y = 100, 100
radius = 35
draw.ellipse((center_x - radius, center_y - radius, center_x + radius, center_y + radius), 
             outline="white", width=3)
            
# Draw horizontal ellipse for globe
draw.ellipse((center_x - radius, center_y - radius // 2, center_x + radius, center_y + radius // 2), 
             outline="white", width=3)

# Draw vertical and horizontal lines through globe
draw.line((center_x - radius, center_y, center_x + radius, center_y), fill="white", width=3)
draw.line((center_x, center_y - radius, center_x, center_y + radius), fill="white", width=3)

# Try to add text "PAIET"
try:
    font = ImageFont.truetype("arial.ttf", 24)
except IOError:
    font = ImageFont.load_default()

# Draw text "PAIET"
text = "PAIET"
text_width = draw.textlength(text, font=font) if hasattr(draw, 'textlength') else 60
draw.text((width // 2 - text_width // 2, height - 40), text, fill="white", font=font)

# Save the image
output_path = 'static/images/logo.png'
image.save(output_path)
print(f"Logo created and saved to {output_path}") 