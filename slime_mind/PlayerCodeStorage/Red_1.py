from slime_mind.models.player_base import PlayerBase
from slime_mind.models.commands import Commands
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
        if target == 0:
            return Commands.DOWN

        start.distance = abs(slime['x']-target['x']) + abs(slime['y']-target['y'])
        start.x = slime['x']
        start.y = slime['y']
        move_commands = [Commands.UP, Commands.RIGHT, Commands.DOWN, Commands.LEFT]
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]

        possible_squares = []
        possible_squares[0] = start
        checked_squares = []
        num_checked=0
        max_steps = 5
        
        for current_square in possible_squares:
            checked = False
            for past_square in checked_squares:
                if past_square.x == current_square.x and past_square.y == current_square.y:
                    checked = True
            if not checked:
                for i in range(len(dx)):
                    if valid_coord(matrix, current_square.x+dx[i], current_square.y+dy[i]):
                        if matrix[current_square.x+dx[i]][current_square.y+dy[i]] == None:
                            square.x = current_square.x+dx[i]
                            square.y = current_square.y+dy[i]
                            square.parent = current_square
                            square.distance = abs(current_square.x-target['x']) + abs(current_square.y-target['y'])
                            square.command = move_commands[i]
                            possible_squares.append(current_square)
                            if square.distance <= start.distance - max_steps:
                                break
            checked_squares.append(current_square)
            if num_checked >= 100:
                break
        
        min_distance = 1000
        for square in checked_squares:
            if square.distance < min_distance:
                min_distance = square.distance
                current_square = square
        
        while current_square.distance < distance - 1:
            current_square = current_square.parent

        return current_square.command
        
    
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
