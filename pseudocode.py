import math

class Player:
    PLAYERS = set()

    def __init__(self):
        self.position = [0, 0]
        self.velocity = [0, 0]
        self.size = 40
        Player.PLAYERS.add(self)
    
    def check_collisions(self):
        # for all other players
        for other_player in Player.PLAYERS - {self}:
            # check for collision, but only once per pair of players
            if id(self) < id(other_player) and self.collides_with(other_player):
                # handle collision
                self.collide(other_player)
    
    def collides_with(self, other):
        # if the distance between the two objects is less than the sum of their radii, they are colliding
        return math.hypot(self.position[0] - other.position[0], self.position[1] - other.position[1]) < self.size + other.size

    def collide(self, other):
        # if two players collide, they die
        pass