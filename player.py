import arcade
from datetime import timedelta
import arcade
import math


class Circle:
    LAYERS = {}

    def __init__(self, position: list, radius, layers = [0]):
        self.position = position
        self.radius = radius
        for layer in layers:
            self.LAYERS.setdefault(layer, set()).add(self)
        self.collisions = set()

    def collides_with(self, other):
        # if the distance between the two objects is less than the sum of their radii, they collide
        return (math.hypot(self.position[0] - other.position[0], self.position[1] - other.position[1]) < self.radius + other.radius)

    @staticmethod
    def update_collisions(layers = None):
        layers = layers or Circle.LAYERS

        # get all circles
        circles = set().union(*layers.values())

        # clear all collisions
        for circle in circles:
            circle.collisions.clear()
        
        # check for collisions between circles in each layer
        for layer in layers.values():
            for circle in layer:
                # ignore current circle, and circles that have already collided with this circle
                for other_circle in layer - {circle} - circle.collisions:
                    if circle.collides_with(other_circle):
                        circle.collisions.add(other_circle)
                        other_circle.collisions.add(circle)


class Player:
    PLAYER_ACCEL = 500
    PLAYER_SPEED = 250
    ELASTIC_COLLISION = True
    SIZE = 25
    PLAYERS = set()

    def __init__(self, position: list, color):
        self.position = position
        self.velocity = [0, 0]
        self.acceleration = [0, 0]
        self.color = color
        self.hitbox = Circle(self.position, self.SIZE)
        self.PLAYERS.add(self)

    @property
    def normalized_accel(self):
        # if both x and y acceleration are nonzero, normalize the acceleration
        if all(self.acceleration):
            return [vel / math.sqrt(2) for vel in self.acceleration]
        return self.acceleration.copy()

    def get_rel_speed(self, other):
        # get the rate at which this player is approaching the other player
        return math.cos(self.get_rel_angle(other)) * (self.velocity[0] - other.velocity[0]) + math.sin(self.get_rel_angle(other)) * (self.velocity[1] - other.velocity[1])
    
    def get_rel_angle(self, other):
        # get the relative angle of this player's position to the other player's position
        return math.atan2(self.position[1] - other.position[1], self.position[0] - other.position[0])

    def update(self, delta_time):
        accel = self.normalized_accel
        
        # set new player velocity
        self.velocity[0] += accel[0] * self.PLAYER_ACCEL * delta_time
        self.velocity[1] += accel[1] * self.PLAYER_ACCEL * delta_time

        # if player is touching another player
        if self.hitbox.collisions:
            for hitbox in self.hitbox.collisions:
                # get the owner of the hitbox
                player = next(player for player in self.PLAYERS if player.hitbox is hitbox)

                # get the relative velocity of this player to the other player
                rel_speed = self.get_rel_speed(player)

                # if this player is approaching the other player
                if rel_speed < 0:
                    # get the relative angle of this player to the other player
                    rel_angle = self.get_rel_angle(player)
                    
                    rel_speed /= 2

                    # add to this player's velocity
                    self.velocity[0] -= math.cos(rel_angle) * rel_speed
                    self.velocity[1] -= math.sin(rel_angle) * rel_speed

                    # add to the other player's velocity
                    player.velocity[0] += math.cos(rel_angle) * rel_speed
                    player.velocity[1] += math.sin(rel_angle) * rel_speed
        
        # limit player velocity to PLAYER_SPEED
        self.velocity[0] = max(min(self.velocity[0], self.PLAYER_SPEED), -self.PLAYER_SPEED)
        self.velocity[1] = max(min(self.velocity[1], self.PLAYER_SPEED), -self.PLAYER_SPEED)
        
        # set new player position
        self.position[0] += self.velocity[0] * delta_time
        self.position[1] += self.velocity[1] * delta_time

        # limit player to bounds of screen, accounting for player radius
        SCREEN_WIDTH, SCREEN_HEIGHT = arcade.get_window().get_size()
        self.position[0] = max(min(self.position[0], SCREEN_WIDTH - self.SIZE), self.SIZE)
        self.position[1] = max(min(self.position[1], SCREEN_HEIGHT - self.SIZE), self.SIZE)

        # if player is touching a wall, stop or bounce
        if self.position[0] == self.SIZE or self.position[0] == SCREEN_WIDTH - self.SIZE:
            self.velocity[0] *= -1 if self.ELASTIC_COLLISION else 0
        if self.position[1] == self.SIZE or self.position[1] == SCREEN_HEIGHT - self.SIZE:
            self.velocity[1] *= -1 if self.ELASTIC_COLLISION else 0

    def draw(self, delta_time):
        color = self.color

        # if player is touching another player, change color
        if self.hitbox.collisions:
            color = arcade.color.WHITE
        
        # Draw the player's circle
        arcade.draw_circle_filled(self.position[0], self.position[1], self.SIZE, color)

def polar_to_rect(radius, angle):
    return [radius * math.cos(angle), radius * math.sin(angle)]

if __name__ == "__main__":
    pass