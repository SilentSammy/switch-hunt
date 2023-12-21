import math

class Player:
    PLAYERS = set()

    def __init__(self):
        self.position = [0, 0]
        self.velocity = [0, 0]
        self.size = 40
        Player.PLAYERS.add(self)
    
    def check_collisions(self):
        # check for collisions with other players
        for other_player in Player.PLAYERS - {self}:
            if self.collides_with(other_player):
                self.collide(other_player)
    
    def collides_with(self, other):
        # if the distance between the two objects is less than the sum of their radii, they collide
        return math.hypot(self.position[0] - other.position[0],self.position[1] - other.position[1]) < self.size + other.size

    def collide(self, other):
        # handle collision, but only once per pair of players
        pass