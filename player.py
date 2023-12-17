import arcade
from datetime import timedelta
import arcade
import math


class Circle:
    LAYERS = {}

    def __init__(self, position: list, radius, layers=[0]):
        self.position = position
        self.radius = radius
        for layer in layers:
            self.LAYERS.setdefault(layer, set()).add(self)
        self.collisions = set()

    def collides_with(self, other):
        # if the distance between the two objects is less than the sum of their radii, they collide
        return (
            math.hypot(
                self.position[0] - other.position[0],
                self.position[1] - other.position[1],
            )
            < self.radius + other.radius
        )

    @staticmethod
    def update_collisions(layers=None):
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
    SIZE = 40
    PLAYERS = set()

    def __init__(self, position: list, sprite):
        self.position = position
        self.velocity = [0, 0]
        self.acceleration = [0, 0]
        self.sprite = sprite
        self.braking = False
        self.hitbox = Circle(self.position, self.SIZE)
        self.PLAYERS.add(self)

    @property
    def effective_accel(self):
        accel = self.acceleration.copy()

        # make sure that the acceleration is not greater than 1
        self.acceleration = [min(max(accel, -1), 1) for accel in self.acceleration]

        # if both x and y acceleration are nonzero, normalize the acceleration
        accel = [vel / math.sqrt(2) for vel in self.acceleration] if all(self.acceleration) else accel

        if self.braking:
            # we define a polar vector with a magnitude of -1 and an angle equal to the angle of the player's velocity
            braking_accel = polar_to_rect(-1, math.atan2(self.velocity[1], self.velocity[0]))

            # if player is moving in the x-axis, and their acceleration in the x-axis is 0 or opposite sign to their velocity in the x-axis, apply braking acceleration to x-axis
            if self.velocity[0] and (not accel[0] or math.copysign(1, accel[0]) != math.copysign(1, self.velocity[0])):
                accel[0] += braking_accel[0]
            
            # if player is moving in the y-axis, and their acceleration in the y-axis is 0 or opposite sign to their velocity in the y-axis, apply braking acceleration to y-axis
            if self.velocity[1] and (not accel[1] or math.copysign(1, accel[1]) != math.copysign(1, self.velocity[1])):
                accel[1] += braking_accel[1]

        return accel

    def get_rel_speed(self, other):
        # get the rate at which this player is approaching the other player
        return math.cos(self.get_rel_angle(other)) * (
            self.velocity[0] - other.velocity[0]
        ) + math.sin(self.get_rel_angle(other)) * (self.velocity[1] - other.velocity[1])

    def get_rel_angle(self, other):
        # get the relative angle of this player's position to the other player's position
        return math.atan2(
            self.position[1] - other.position[1], self.position[0] - other.position[0]
        )

    def update_pos(self, delta_time):
        # set new player position
        self.position[0] += self.velocity[0] * delta_time
        self.position[1] += self.velocity[1] * delta_time

        # limit player to bounds of screen, accounting for player radius
        SCREEN_WIDTH, SCREEN_HEIGHT = arcade.get_window().get_size()
        self.position[0] = max(
            min(self.position[0], SCREEN_WIDTH - self.SIZE), self.SIZE
        )
        self.position[1] = max(
            min(self.position[1], SCREEN_HEIGHT - self.SIZE), self.SIZE
        )

    def update_vel(self, delta_time):
        # accelerate player
        accel = self.effective_accel
        prev_velocity = self.velocity.copy()
        self.velocity = [ self.velocity[0] + accel[0] * self.PLAYER_ACCEL * delta_time, self.velocity[1] + accel[1] * self.PLAYER_ACCEL * delta_time ]

        # if the player is braking, and the player's velocity has changed direction, set the velocity to 0
        if self.braking and any(prev_velocity) and any(self.velocity):
            if math.copysign(1, prev_velocity[0]) != math.copysign(1, self.velocity[0]):
                self.velocity[0] = 0
            if math.copysign(1, prev_velocity[1]) != math.copysign(1, self.velocity[1]):
                self.velocity[1] = 0

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

                    if not self.ELASTIC_COLLISION:
                        rel_speed *= 0.5

                    # add to this player's velocity
                    self.velocity[0] -= math.cos(rel_angle) * rel_speed
                    self.velocity[1] -= math.sin(rel_angle) * rel_speed

                    # add to the other player's velocity
                    player.velocity[0] += math.cos(rel_angle) * rel_speed
                    player.velocity[1] += math.sin(rel_angle) * rel_speed

        # limit player velocity to PLAYER_SPEED
        self.velocity[0] = max(min(self.velocity[0], self.PLAYER_SPEED), -self.PLAYER_SPEED)
        self.velocity[1] = max(min(self.velocity[1], self.PLAYER_SPEED), -self.PLAYER_SPEED)

        # if player is touching a wall, stop or bounce
        SCREEN_WIDTH, SCREEN_HEIGHT = arcade.get_window().get_size()
        if (self.position[0] == self.SIZE or self.position[0] == SCREEN_WIDTH - self.SIZE):
            self.velocity[0] *= -1 if self.ELASTIC_COLLISION else 0
        if (self.position[1] == self.SIZE or self.position[1] == SCREEN_HEIGHT - self.SIZE):
            self.velocity[1] *= -1 if self.ELASTIC_COLLISION else 0

    def draw(self, delta_time):
        # Draw the player's sprite oriented in the direction of the player's velocity
        self.sprite.center_x = self.position[0]
        self.sprite.center_y = self.position[1]

        # if the player is not moving, don't rotate the sprite
        if any(self.velocity):
            self.sprite.angle = (
                math.degrees(math.atan2(self.velocity[1], self.velocity[0])) - 90
            )
        self.sprite.draw()

        # Draw the player's circle
        arcade.draw_circle_outline(
            self.position[0], self.position[1], self.SIZE, arcade.color.WHITE
        )

    def __str__(self):
        # we return every attribute and property of the player (rounded to two decimals) separated by new lines
        return "\n".join(
            [
                f"Position: {self.position[0]:.2f}, {self.position[1]:.2f}",
                f"Velocity: {self.velocity[0]:.2f}, {self.velocity[1]:.2f}",
                f"Acceleration: {self.acceleration[0]:.2f}, {self.acceleration[1]:.2f}",
                f"Effective Acceleration: {self.effective_accel[0]:.2f}, {self.effective_accel[1]:.2f}",
                f"Braking: {self.braking}",
            ]
        )


def polar_to_rect(radius, angle):
    return [radius * math.cos(angle), radius * math.sin(angle)]


if __name__ == "__main__":
    pass
