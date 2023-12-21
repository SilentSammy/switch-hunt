import arcade
from datetime import timedelta
import arcade
import math

class Player:
    PLAYER_ACCEL = 500
    PLAYER_SPEED = 250
    ELASTIC_COLLISION = True
    PLAYERS = set()
    PLAYER_LIVES = 3

    def __init__(self, position: list, sprite, role = 1):
        self.position = position
        self.velocity = [0, 0]
        self.acceleration = [0, 0]
        self.sprite = sprite
        self.braking = False
        self.PLAYERS.add(self)
        self.size = 40
        self._hp = 1
    
    @staticmethod
    def handle_collision(player, other_player):
        pass
    
    @property
    def hp(self):
        return round(self._hp, 2)

    @hp.setter
    def hp(self, value):
        self._hp = max(min(value, 1), 0)

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
            min(self.position[0], SCREEN_WIDTH - self.size), self.size
        )
        self.position[1] = max(
            min(self.position[1], SCREEN_HEIGHT - self.size), self.size
        )

    def update(self, delta_time):
        self.hp -= 0.1 * delta_time
        self.accelerate(delta_time)
        self.check_collisions()
        self.check_wall_collision()
        self.limit_speed()
    
    def accelerate(self, delta_time):
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

    def check_collisions(self):
        for other_player in Player.PLAYERS - {self}:
            if id(self) < id(other_player) and self.collides_with(other_player):
                self.collide(other_player)

    def collides_with(self, other):
        return math.hypot(self.position[0] - other.position[0],self.position[1] - other.position[1]) < self.size + other.size

    def collide(self, other_player):
        # get the relative velocity of this player to the other player
        rel_speed = self.get_rel_speed(other_player)

        # if this player is approaching the other player
        if rel_speed < 0:
            # get the relative angle of this player to the other player
            rel_angle = self.get_rel_angle(other_player)

            if not self.ELASTIC_COLLISION:
                rel_speed *= 0.5

            # define a bounce vector
            bounce = [math.cos(rel_angle) * rel_speed, math.sin(rel_angle) * rel_speed]

            # subtract bounce vector from this player's velocity
            self.velocity = [self.velocity[i] - bounce[i] for i in range(2)]
            
            # add bounce vector to other player's velocity
            other_player.velocity = [other_player.velocity[i] + bounce[i] for i in range(2)]

    def check_wall_collision(self):
        # if player is touching a wall, stop or bounce
        SCREEN_WIDTH, SCREEN_HEIGHT = arcade.get_window().get_size()
        if (self.position[0] == self.size or self.position[0] == SCREEN_WIDTH - self.size):
            self.velocity[0] *= -1 if self.ELASTIC_COLLISION else 0
        if (self.position[1] == self.size or self.position[1] == SCREEN_HEIGHT - self.size):
            self.velocity[1] *= -1 if self.ELASTIC_COLLISION else 0

    def limit_speed(self):
        # limit velocity magnitude to PLAYER_SPEED
        speed = math.hypot(self.velocity[0], self.velocity[1])
        if speed > self.PLAYER_SPEED:
            self.velocity = [self.velocity[0] * self.PLAYER_SPEED / speed, self.velocity[1] * self.PLAYER_SPEED / speed]

    def draw(self, delta_time):
        # Draw the player's sprite oriented in the direction of the player's velocity
        self.sprite.center_x = self.position[0]
        self.sprite.center_y = self.position[1]

        # if the player is not moving, don't rotate the sprite
        if any(self.velocity):
            self.sprite.angle = math.degrees(math.atan2(self.velocity[1], self.velocity[0])) - 90
        self.sprite.draw()

        # define an RGB color based on the player's hp
        hp_color = [int(255 * (1 - self.hp)), int(255 * self.hp), 0]


        # draw the player's hp as an arc around the player
        arcade.draw_arc_outline(self.position[0], self.position[1], self.size * 2, self.size * 2, hp_color, 0, 360 * self.hp, 10)

    def lose_life(self):
        self.hp -= 1/self.PLAYER_LIVES

    def __str__(self):
        # we return every attribute and property of the player (rounded to two decimals) separated by new lines
        return "\n".join(
            [
                f"Position: {self.position[0]:.2f}, {self.position[1]:.2f}",
                f"Velocity: {self.velocity[0]:.2f}, {self.velocity[1]:.2f}",
                f"Acceleration: {self.acceleration[0]:.2f}, {self.acceleration[1]:.2f}",
                f"Effective Acceleration: {self.effective_accel[0]:.2f}, {self.effective_accel[1]:.2f}",
                f"Braking: {self.braking}",
                f"HP: {self.hp:.2f}",
            ]
        )

def polar_to_rect(radius, angle):
    return [radius * math.cos(angle), radius * math.sin(angle)]

if __name__ == "__main__":
    pass
