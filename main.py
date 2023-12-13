import arcade
import math
from player import Player, Circle

# Set up the window dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "My Arcade Game"

# Player settings
PLAYER_SPEED = 250
PLAYER_ACCEL = 500
keybindings = [
    {
        arcade.key.W: (0, 1),  # Up
        arcade.key.A: (-1, 0),  # Left
        arcade.key.S: (0, -1),  # Down
        arcade.key.D: (1, 0)  # Right
    },
    {
        arcade.key.UP: (0, 1),  # Up
        arcade.key.LEFT: (-1, 0),  # Left
        arcade.key.DOWN: (0, -1),  # Down
        arcade.key.RIGHT: (1, 0)  # Right
    },
    {
        arcade.key.T: (0, 1),  # Up
        arcade.key.F: (-1, 0),  # Left
        arcade.key.G: (0, -1),  # Down
        arcade.key.H: (1, 0)  # Right
    },
    {
        arcade.key.I: (0, 1),  # Up
        arcade.key.J: (-1, 0),  # Left
        arcade.key.K: (0, -1),  # Down
        arcade.key.L: (1, 0)  # Right
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
players = [Player(starting_pos[i], colors[i]) for i in range(4)]

# Create the game window
window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

# Set up any additional game initialization here

def setup():
    # Set up any game-specific initialization here
    # players[0].velocity[0] = 100
    # players[1].velocity[0] = -100
    pass

def on_draw(delta_time):
    arcade.start_render()
    for player in players:
        player.draw(delta_time)

def update(delta_time):
    # Update each player's position
    for player in players:
        player.update_pos(delta_time)
    
    # update all hitboxes
    Circle.update_collisions()

    # Update each player's velocity
    for player in players:
        player.update_vel(delta_time)   

def on_key_press(symbol, modifiers):
    for i, player in enumerate(players):
        for key, vector in keybindings[i].items():
            if symbol == key:
                player.acceleration[0] += vector[0]
                player.acceleration[1] += vector[1]
                break

def on_key_release(symbol, modifiers):
    for i, player in enumerate(players):
        for key, vector in keybindings[i].items():
            if symbol == key:
                player.acceleration[0] -= vector[0]
                player.acceleration[1] -= vector[1]
                break

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
