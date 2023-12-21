import arcade
import os
import time

# Path to the sprite image file
sprite_path = "sprites\prey\crab1.png"
last_modified = os.path.getmtime(sprite_path)

pos = [400, 300]
size = 100

# Function to load and display the sprite
def load_sprite(delta_time):
    # Clear the window
    arcade.start_render()
    arcade.set_background_color(arcade.color.WHITE_SMOKE)
    
    # Load the sprite image
    path = sprite_path
    texture = arcade.load_texture(path)
    shortest_axis = min(texture.width, texture.height)
    desired_size = size * 3
    scale_factor = desired_size / shortest_axis
    sprite = arcade.Sprite(path, scale=scale_factor)

    # Set the position of the sprite
    sprite.center_x = pos[0]
    sprite.center_y = pos[1]

    # Draw the sprite
    sprite.draw()

    # Draw the sprite's hitbox
    arcade.draw_circle_outline(pos[0], pos[1], size, arcade.color.NEON_GREEN)

    print(f"Sprite loaded: {time.time()}")

# Create the Arcade window
window = arcade.Window(800, 600, "Sprite Viewer")

arcade.schedule(load_sprite, 1 / 2)

# Run the Arcade event loop
arcade.run()
