import sys
from PIL import Image, ImageFilter
import os
from PIL import Image

def remove_semi_transparent_pixels(image_path, radius):
    with Image.open(image_path) as img:
        img = img.convert("RGBA")  # Ensure image is in RGBA format
        pixels = img.load()  # Load pixel data

        width, height = img.size
        for x in range(width):
            for y in range(height):
                r, g, b, a = pixels[x, y]
                if 1 <= a <= 254:
                    # Check surrounding pixels
                    opaque_neighbors = False
                    for dx in range(-radius, radius + 1):
                        for dy in range(-radius, radius + 1):
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < width and 0 <= ny < height:
                                nr, ng, nb, na = pixels[nx, ny]
                                if na == 255:
                                    opaque_neighbors = True
                                    break
                        if opaque_neighbors:
                            break
                    
                    if not opaque_neighbors:
                        # Make the pixel fully transparent
                        pixels[x, y] = (r, g, b, 0)

        # Split the path and filename
        dir_name, file_name = os.path.split(image_path)
        base_name, ext = os.path.splitext(file_name)

        # Construct new file path
        new_file_name = "processed_" + base_name + ext
        new_file_path = os.path.join(dir_name, new_file_name)

        # Save the processed image
        img.save(new_file_path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python remove_semi_transparent.py <input_image_path> [radius]")
    else:
        input_path = sys.argv[1]
        radius = 3
        remove_semi_transparent_pixels(input_path, radius)
