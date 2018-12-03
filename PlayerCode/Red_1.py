from models.player_base import PlayerBase
from models.commands import Commands
import random

# Alex's code started 12/1/2018
# Based on 6-Pack code this code will use a 5 turn movement evaluation 
# for path finding, rush to 6 slimes, split when health is low, and 
# merge at the end of the game
class Player(PlayerBase):
    def __init__(self, player_id):
        super().__init__(id, "Red 1: King Maker", 'images/red/red_1.png', 'default')
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
                        if gamepiece['player_id'] == self.id:
                            self.friends.append(gamepiece)
                        else:
                            self.enemies.append(gamepiece)
                    if gamepiece['type'] == 'PLANT':
                        self.plants.append(gamepiece)

    # TODO Retrun the direction to move to the target by evaluating a route of 5 steps
    def a_star(self, target, slime, matrix, valid_coord):
        distance = abs(slime['x']-target['x']) + abs(slime['y']-target['y'])
        move_commands = [Commands.UP, Commands.RIGHT, Commands.DOWN, Commands.LEFT]
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]

        possibe_square_x= []
        possibe_square_y=[]
        possible_square_distance=[]
        possible_square_command=[]

        for i in range(len(dx)):
            print('test1')
            if valid_coord(matrix, slime['x']+dx[i], slime['y']+dy[i]):
                print('test2')
                if matrix[slime['x']+dx[i]][slime['y']+dy[i]] == None:
                    print('test3')
                    possibe_square_x.append(slime['x']+dx[i])
                    possibe_square_y.append(slime['y']+dy[i])
                    possible_square_distance.append(abs(slime['x']+dx[i]-target['x']) + abs(slime['y']+dy[i]-target['y']))
                    possible_square_command.append(move_commands[i])

        if len(possible_square_distance) == 0:
            return Commands.UP
        square_index = possible_square_distance.index(min(possible_square_distance))

        return possible_square_command[square_index]
        
    
    # Determine if the targeted location is a valid location
    def valid_coord(self, state, x, y):
        return ((0 <= x < len(state)) and (0 <= y < len(state[0])))

    # All AI must have this line
    def command_slime(self, state, slime, turn):
        self.find_stuff(state)

        # Check if level is high and health is low
        if slime['current_hp'] <= 20:
            if slime['level'] >= 8:
                return Commands.SPLIT


        # check each direction for a slime then a palnt, if a slime is found check if it is on our team
        bite_option = [Commands.BITELEFT, Commands.BITERIGHT, Commands.BITEUP, Commands.BITEDOWN]
        dx = [slime['x']-1, slime['x']+1, slime['x'], slime['x']]
        dy = [slime['y'], slime['y'], slime['y']+1, slime['y']-1]
        
        # check for enemy slimes
        for i in range(4):
            if self.valid_coord(state, dx[i], dy[i]) and state[dx[i]][dy[i]] is not None:
                if state[dx[i]][dy[i]]['type'] == 'SLIME':
                    if state[dx[i]][dy[i]]['player_id'] != slime['player_id']:
                        return bite_option[i]

        # check for plants
        for i in range(4):
            if self.valid_coord(state, dx[i], dy[i]) and state[dx[i]][dy[i]] is not None:
                if state[dx[i]][dy[i]]['type'] == 'PLANT':
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
        enemy_power = 0

        for friend in self.friends:
            friend_power += friend['level']
        
        for enemy in self.enemies:
            enemy_power += enemy['level']

        if friend_power > 60:
            target = nearest_enemy
        elif friend_power > enemy_power and nearest_enemy_distance < 10:
            target = nearest_enemy
        elif len(self.plants) > 0:
            target = nearest_plant
        else:
            target = nearest_enemy

        command_call = self.a_star(target, slime, state, self.valid_coord)

        return command_call
