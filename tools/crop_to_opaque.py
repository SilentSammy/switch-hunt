from PIL import Image
import sys
import uuid
import os
import os

path = sys.argv[1]

def crop_to_opaque(img_path):
    with Image.open(img_path) as img:
        # Convert image to RGBA if it's not
        img = img.convert("RGBA")

        # Get the bounding box
        bbox = img.getbbox()

        # Crop the image to the bounding box
        cropped_img = img.crop(bbox)
        return cropped_img

# Usage example
cropped_image = crop_to_opaque(path)
#cropped_image.show()  # Display the cropped image
# Generate a unique file name
new_path = os.path.join(os.path.dirname(path), 'image.png')
print(new_path)
cropped_image.save(new_path)  # Optionally, save the cropped image
