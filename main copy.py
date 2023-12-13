import arcade
import math
from player import Player

# Set up the window dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "My Arcade Game"

# Player settings
PLAYER_SPEED = 200
PLAYER_ACCEL = 400
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
colors = [arcade.color.RED, arcade.color.GREEN, arcade.color.BLUE, arcade.color.YELLOW]
# x, y, x_vel, y_vel, x_accel, y_accel
players = [[0, 0, 0, 0, 0, 0] for _ in range(4)]

# Create the game window
window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

# Set up any additional game initialization here

def setup():
    # Set up any game-specific initialization here
    pass

def on_draw(delta_time):
    # Clear the screen and start drawing
    arcade.start_render()

    # Add your drawing code here
    for i, player in enumerate(players):
        x, y = player[0], player[1]
        color = colors[i % len(colors)]
        arcade.draw_rectangle_filled(x, y, 50, 50, color)

def update(delta_time):
    for player in players:
        # set new player acceleration, limited to 1
        player_accel = player[4:6]
        if all(player_accel):
            player_accel = [vel / math.sqrt(2) for vel in player_accel]
        
        # set new player velocity
        player[2] += player_accel[0] * delta_time * PLAYER_ACCEL
        player[3] += player_accel[1] * delta_time * PLAYER_ACCEL
        
        # limit player velocity to PLAYER_SPEED
        player[2] = max(min(player[2], PLAYER_SPEED), -PLAYER_SPEED)
        player[3] = max(min(player[3], PLAYER_SPEED), -PLAYER_SPEED)
        
        # set new player position
        player[0] += player[2] * delta_time
        player[1] += player[3] * delta_time

        # limit player to bounds of screen
        player[0] = max(min(player[0], SCREEN_WIDTH), 0)
        player[1] = max(min(player[1], SCREEN_HEIGHT), 0)

def on_key_press(symbol, modifiers):
    for i, player in enumerate(players):
        for key, vector in keybindings[i].items():
            if symbol == key:
                player[4] += vector[0]
                player[5] += vector[1]
                break

def on_key_release(symbol, modifiers):
    for i, player in enumerate(players):
        for key, vector in keybindings[i].items():
            if symbol == key:
                player[4] -= vector[0]
                player[5] -= vector[1]
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
