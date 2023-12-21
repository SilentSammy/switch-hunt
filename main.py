import arcade
import math
from player import Player
import os
import glob

# Set up the window dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "My Arcade Game"

# Player settings
keybindings = [
    {
        "accel": {
            arcade.key.W: (0, 1),  # Up
            arcade.key.A: (-1, 0),  # Left
            arcade.key.S: (0, -1),  # Down
            arcade.key.D: (1, 0)  # Right
        },
        "brake": arcade.key.Q
    },
    {
        "accel": {
            arcade.key.UP: (0, 1),  # Up
            arcade.key.LEFT: (-1, 0),  # Left
            arcade.key.DOWN: (0, -1),  # Down
            arcade.key.RIGHT: (1, 0)  # Right
        },
        "brake": arcade.key.SPACE
    },
    {
        "accel": {
            arcade.key.T: (0, 1),  # Up
            arcade.key.F: (-1, 0),  # Left
            arcade.key.G: (0, -1),  # Down
            arcade.key.H: (1, 0)  # Right
        },
        "brake": arcade.key.R
    },
    {
        "accel": {
            arcade.key.I: (0, 1),  # Up
            arcade.key.J: (-1, 0),  # Left
            arcade.key.K: (0, -1),  # Down
            arcade.key.L: (1, 0)  # Right
        },
        "brake": arcade.key.U
    }
]
colors = [
    arcade.color.RED,
    arcade.color.GREEN,
    arcade.color.BLUE,
    arcade.color.YELLOW
]
starting_pos = [
    [SCREEN_WIDTH / 4, SCREEN_HEIGHT / 4],
    [SCREEN_WIDTH * 3 / 4, SCREEN_HEIGHT / 4],
    [SCREEN_WIDTH / 4, SCREEN_HEIGHT * 3 / 4],
    [SCREEN_WIDTH * 3 / 4, SCREEN_HEIGHT * 3 / 4]
]
players = []

# Create the game window
window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

def setup():
    # load sprites
    sprites = []
    for path in glob.glob("sprites/prey/*.png"):
        # Your code here
        texture = arcade.load_texture(path)
        shortest_axis = min(texture.width, texture.height)
        desired_size = 40 * 3
        scale_factor = desired_size / shortest_axis
        sprites.append(arcade.Sprite(path, scale=scale_factor))

    global players
    players = [Player(starting_pos[i], sprites[i]) for i in range(4)]

def on_draw(delta_time):
    arcade.start_render()
    arcade.set_background_color(arcade.color.OCEAN_BOAT_BLUE)
    for player in players:
        player.draw(delta_time)
    
    # Generate a string with all the player's data
    output = ""
    for i, player in enumerate(players):
        output += f"Player {i + 1}:\n{player}\n\n"

    # Display text in the top left corner of the screen
    arcade.draw_text(output, 5, SCREEN_HEIGHT - 15, arcade.color.WHITE, 10, multiline=True, width=300)

def update(delta_time):
    # Update each player's position
    for player in players:
        player.update_pos(delta_time)
    
    # Update players
    for player in players:
        player.update(delta_time)

def on_key_press(symbol, modifiers):
    # print the key that was pressed
    print(f"Key pressed: {symbol}")

    for i, player in enumerate(players):
        for key, vector in keybindings[i]["accel"].items():
            if symbol == key:
                player.acceleration = [ player.acceleration[i] + vector[i] for i in range(2) ]
                break
        if symbol == keybindings[i]["brake"]:
            player.braking = True

def on_key_release(symbol, modifiers):
    # print the key that was released
    print(f"Key released: {symbol}")

    for i, player in enumerate(players):
        for key, vector in keybindings[i]["accel"].items():
            if symbol == key:
                player.acceleration = [ player.acceleration[i] - vector[i] for i in range(2) ]
                break
        if symbol == keybindings[i]["brake"]:
            player.braking = False

def main():
    # Call the setup function to initialize the game
    setup()

    # Set up the game window to call the on_draw function every frame
    arcade.schedule(on_draw, 1 / 60)

    # Set up the game window to call the update function every frame
    arcade.schedule(update, 1 / 60)
    
    # Set up the game window to call the on_key_press function when a key is pressed
    window.on_key_press = on_key_press
    window.on_key_release = on_key_release

    # Run the game
    arcade.run()

if __name__ == "__main__":
    main()
