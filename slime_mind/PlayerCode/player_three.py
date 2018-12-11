from slime_mind.models.player_base import PlayerBase
from slime_mind.models.commands import Commands
import random
import time

class Player(PlayerBase):
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
                        if gamepiece['player_id'] == self.id:
                            self.friends.append(gamepiece)
                        else:
                            self.enemies.append(gamepiece)
                    if gamepiece['type'] == 'PLANT':
                        self.plants.append(gamepiece)

    def valid_coord(self, state, x, y):
        return ((0 <= x < len(state)) and (0 <= y < len(state[0])))

    def command_slime(self, state, slime, turn):
        self.find_stuff(state)

        # num_thing= random.randint(1,3)
        # num_thing = num_thing/100
        # print('slime is trying to wait', num_thing)
        # time.sleep(num_thing)

        # split only up to 6 total slimes
        if len(self.friends) <= 20 and slime['level'] >= 4:
            return Commands.SPLIT

        # bite nearby plants or enemies
        bite_option = [Commands.BITELEFT, Commands.BITERIGHT, Commands.BITEUP, Commands.BITEDOWN]
        dx = [slime['x']-1, slime['x']+1, slime['x'], slime['x']]
        dy = [slime['y'], slime['y'], slime['y']+1, slime['y']-1]
        for i in range(4):
            if self.valid_coord(state, dx[i], dy[i]):
                neighbor = state[dx[i]][dy[i]]
                if neighbor in self.plants or neighbor in self.enemies:
                    return bite_option[i]

        # Move randomly
        move_options = [Commands.LEFT,Commands.RIGHT,Commands.UP,Commands.DOWN]
        return random.choice(move_options)
