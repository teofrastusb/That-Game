from models.player_base import PlayerBase
from models.commands import Commands
import random

class Player(PlayerBase):
    def __init__(self, player_id):
        super().__init__(id, "6 pack attack")
        self.id = player_id
        self.friends = []
        self.enemies =[]
        self.plants =[]

    def find_stuff(self, matrix):
        self.friends =[]
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

    # Retrun the direction to move to the target
    def a_star(self, target, slime):
        if target != 0:
            if slime['x'] > target['x']:
                return Commands.LEFT
            elif slime['x'] < target['x']:
                return Commands.RIGHT
            elif slime['y'] > target['y']:
                return Commands.DOWN
            elif slime['y'] < target['y']:
                return Commands.UP

    def valid_coord(self, state, x, y):
        return ((0 <= x < len(state)) and (0 <= y < len(state[0])))

    # All AI must have this line
    def command_slime(self, state, slime, turn):
        self.find_stuff(state)

        # check each direction for a plant then a slime, if a slime is found check if it is on our team
        bite_option = [Commands.BITELEFT, Commands.BITERIGHT, Commands.BITEUP, Commands.BITEDOWN]
        dx = [slime['x']-1, slime['x']+1, slime['x'], slime['x']]
        dy = [slime['y'], slime['y'], slime['y']+1, slime['y']-1]
        
        for i in range(4):
            if self.valid_coord(state, dx[i], dy[i]) and state[dx[i]][dy[i]] is not None:
                if state[dx[i]][dy[i]]['type'] == 'PLANT':
                    return bite_option[i]
                elif state[dx[i]][dy[i]]['type'] == 'SLIME':
                    if state[dx[i]][dy[i]]['player'] != slime['player']:
                        return bite_option[i]

        if len(self.friends) < 6:
            if slime['level'] >= 4:
                return Commands.SPLIT

        # Move with a purpose
        # Find nearest plant
        nearest_plant = 0
        plants_checked = 0
        nearest_plant_distance = 10000
        for plant in self.plants:
            plants_checked += 1
            distance = abs(slime['x']-plant['x'])+abs(slime['y']-plant['y'])
            if nearest_plant_distance > distance:
                nearest_plant_distance = distance
                nearest_plant = plant

        # Find nearest enemy
        nearest_enemy= 0
        nearest_enemy_distance = 10000
        for enemy in self.enemies:
            distance = abs(slime['x']-enemy['x']) + abs(slime['y']-enemy['y'])
            if nearest_enemy_distance > distance:
                nearest_enemy_distance = distance
                nearest_enemy = enemy

        # Determine if there are enough friends to attack
        target = 0

        friend_power=0
        for friend in self.friends:
            friend_power += friend['level']

        if friend_power < 60 and len(self.plants) > 0:
            target = nearest_plant
        else:
            target = nearest_enemy

        command_call = self.a_star(target, slime)

        return command_call
