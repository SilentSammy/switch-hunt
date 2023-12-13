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

    @property
    def vel_mag(self):
        return math.hypot(*self.velocity)
    
    @vel_mag.setter
    def vel_mag(self, value):
        self.velocity = [vel / self.vel_mag * value for vel in self.velocity]
    
    @property
    def vel_angle(self):
        return math.atan2(*self.velocity)
    
    @vel_angle.setter
    def vel_angle(self, value):
        self.velocity = [self.vel_mag * math.cos(value), self.vel_mag * math.sin(value)]

    def update(self, delta_time):
        accel = self.normalized_accel
        
        # set new player velocity
        self.velocity[0] += accel[0] * self.PLAYER_ACCEL * delta_time
        self.velocity[1] += accel[1] * self.PLAYER_ACCEL * delta_time
        
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
        
        # if player is touching another player, and their relative velocity is positive, make them bounce
        if self.hitbox.collisions:
            for other in self.hitbox.collisions:
                # get hitbox owner
                other = next(filter(lambda player: player.hitbox is other, self.PLAYERS))

                # calculate relative velocity
                rel_vel = [self.velocity[i] - other.velocity[i] for i in range(2)]

                # if relative velocity magnitude is positive
                if math.hypot(*rel_vel) > 0:
                    # calculate angle of incidence
                    angle = math.atan2(other.position[1] - self.position[1], other.position[0] - self.position[0])

                    # calculate angle of reflection
                    new_angle = 2 * angle - self.vel_angle

                    # set new velocities
                    self.vel_angle = new_angle
                    other.vel_angle = new_angle + math.pi

    def draw(self, delta_time):
        color = self.color

        # if player is touching another player, change color
        if self.hitbox.collisions:
            color = arcade.color.WHITE
        
        # Draw the player's circle
        arcade.draw_circle_filled(self.position[0], self.position[1], self.SIZE, color)

if __name__ == "__main__":
    pass