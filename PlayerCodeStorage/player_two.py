from models.player_base import PlayerBase
from models.commands import Commands
import random

class Player(PlayerBase):
    # example player AI
    def __init__(self, id):
        super().__init__(id, "bite or move randomly", 'default', 'default')
        self.friends = []
        self.enemies =[]
        self.plants =[]

    def find_stuff(self, matrix):
        self.friends = []
        self.enemies =[]
        self.plants =[]
        for x in range(len(matrix)):
            for y in range(len(matrix[x])):
                gamepiece = matrix[x][y]
                if gamepiece is not None:
                    if gamepiece['type'] == 'SLIME':
                        if gamepiece['player'] == self.id:
                            self.friends.append(gamepiece)
                        else:
                            self.enemies.append(gamepiece)
                    if gamepiece['type'] == 'PLANT':
                        self.plants.append(gamepiece)
    
    # bite if enemy or plant is near, otherwise move randomly
    def command_slime(self, state, slime, turn):
        self.find_stuff(state)

        # check each direction for a plant then a slime, if a slime is found check if it is on our team
        if slime['x'] != 0:
            neighbor = state[slime['x']-1][slime['y']]
            if neighbor in self.enemies or neighbor in self.plants:
                return Commands.BITELEFT

        if slime['x'] != len(state)-1:
            neighbor = state[slime['x']+1][slime['y']]
            if neighbor in self.enemies or neighbor in self.plants:
                return Commands.BITERIGHT

        if slime['y'] != 0:
            neighbor = state[slime['x']][slime['y'] - 1]
            if neighbor in self.enemies or neighbor in self.plants:
                return Commands.BITEDOWN

        if slime['y'] != len(state[0]) - 1:
            neighbor = state[slime['x']][slime['y'] + 1]
            if neighbor in self.enemies or neighbor in self.plants:
                return Commands.BITEUP

        if slime['level'] >= 5:
            return Commands.SPLIT

        # Move randomly
        move_options = [Commands.LEFT,Commands.RIGHT,Commands.UP,Commands.DOWN]
        return random.choice(move_options)
