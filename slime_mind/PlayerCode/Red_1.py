from slime_mind.models.player_base import PlayerBase
from slime_mind.models.commands import Commands
import random

# Alex's code started 12/1/2018
# Based on 6-Pack code this code will use a 5 turn movement evaluation 
# for path finding, rush to 6 slimes, split when health is low, and 
# merge at the end of the game
class Player(PlayerBase):
    def __init__(self, player_id):
        super().__init__(player_id, "Red 1: King Maker", 'images/red_1.png')
        self.friends = []
        self.nearest_friend = 0
        self.enemies =[]
        self.nearest_enemy = 0
        self.plants =[]
        self.nearest_plant = 0
        self.merge_time = False

    def find_stuff(self, matrix, slime):
        self.friends =[]
        self.enemies =[]
        self.plants =[]

        self.nearest_friend = 0
        self.nearest_enemy = 0
        self.nearest_plant = 0

        nearest_friend_distance = 1000
        nearest_enemy_distance = 1000
        nearest_plant_distance = 1000
        distance = 0

        for x in range(len(matrix)):
            for y in range(len(matrix[x])):
                gamepiece = matrix[x][y]
                if gamepiece is not None:
                    if gamepiece['type'] == 'SLIME':
                        if gamepiece['player_id'] == self.id and gamepiece['id'] != slime['id']:
                            self.friends.append(gamepiece)
                            distance = abs(slime['x']-gamepiece['x']) + abs(slime['y']-gamepiece['y'])
                            if distance < nearest_friend_distance:
                                self.nearest_friend = gamepiece
                                nearest_friend_distance = distance

                        else:
                            self.enemies.append(gamepiece)
                            distance = abs(slime['x']-gamepiece['x']) + abs(slime['y']-gamepiece['y'])
                            if distance < nearest_enemy_distance:
                                self.nearest_enemy = gamepiece
                                nearest_enemy_distance = distance
                    if gamepiece['type'] == 'PLANT':
                        self.plants.append(gamepiece)
                        distance = abs(slime['x']-gamepiece['x']) + abs(slime['y']-gamepiece['y'])
                        if distance < nearest_plant_distance:
                            self.nearest_plant = gamepiece
                            nearest_plant_distance = distance

    # Retrun the direction to move to the target
    def a_star(self, target, slime, matrix, valid_coord):
        if target == 0:
            return Commands.DOWN

        if target['type'] == 'PLANTS' and len(self.plants) == 0:
            return Commands.DOWN

        if target['type'] == 'SLIME' and len(self.enemies) == 0:
            return Commands.DOWN

        class Square():
            def __init__(self):
                self.distance = 0
                self.cost = 0
                self.score = 0
                self.command = 0
                self.parent = None
        # Create a starting square at the slimes locaiton
        start = Square()
        start.distance = (slime['x']-target['x'])**2 + (slime['y']-target['y'])**2
        start.x = slime['x']
        start.y = slime['y']
        start.cost = 0
        start.command = Commands.SPLIT
        move_commands = [Commands.UP, Commands.RIGHT, Commands.DOWN, Commands.LEFT]
        dx = [0, 1, 0, -1]
        dy = [1, 0, -1, 0]

        # Create list to hold squares to be checked, and list to hold previously checked squares
        possible_squares = []
        checked_squares = []

        # Add starting square to list to be checked
        possible_squares.append(start)

        # Tweak these to limit calculation time
        max_iterations=10
        max_steps = 5
        iterations = 0

        # While there are still squares to check
        while len(possible_squares)>0:

            iterations += 1

            # Take the first square of the possilbe list
            current_square = possible_squares[0]
            current_index = 0

            # Check the possible list for a square with a lower score
            for i in range(len(possible_squares)):
                if possible_squares[i].score < current_square.score:
                    current_square = possible_squares[i]
                    current_index = i
            
            # Pop current off open list, add to closed list
            possible_squares.pop(current_index)
            checked_squares.append(current_square)

            # If the current_square is the target square then return the first command to get to it
            if target['x'] == current_square.x and target['y'] == current_square.y:
                command_return = []
                while current_square.command is not Commands.SPLIT:
                    command_return = current_square
                    current_square = current_square.parent
                return command_return
            
            # If the cost of the current square is over the max_steps exit
            if current_square.cost > max_steps:
                command_return = current_square.command
                while current_square.command is not Commands.SPLIT:
                    command_return = current_square.command
                    current_square = current_square.parent
                return command_return

            # Cycle through near by squares for possible children
            children = []
            for i in range(len(dx)):
                if valid_coord(matrix, current_square.x+dx[i], current_square.y+dy[i]):
                    if matrix[current_square.x+dx[i]][current_square.y+dy[i]] == None:
                        square = Square()
                        square.x = current_square.x+dx[i]
                        square.y = current_square.y+dy[i]
                        square.parent = current_square
                        square.distance = (current_square.x-target['x'])**2 + (current_square.y-target['y'])**2
                        square.cost = current_square.cost + 1
                        square.score = square.distance + square.cost
                        square.command = move_commands[i]
                        children.append(square)

            # Loop through children
            for child in children:

                # Child is on the closed list
                for checked in checked_squares:
                    if child == checked:
                        continue

                # Child is already in the open list
                for possible in possible_squares:
                    if child == possible and child.score > possible.score:
                        continue

                # Add the child to the open list
                possible_squares.append(child)

            if iterations > max_iterations:
                if current_square.cost > max_steps:
                    command_return = current_square.command
                    while current_square.command is not Commands.SPLIT:
                        command_return = current_square.command
                        current_square = current_square.parent
                    return command_return
        
    
    # Determine if the targeted location is a valid location
    def valid_coord(self, state, x, y):
        return ((0 <= x < len(state)) and (0 <= y < len(state[0])))

    # All AI must have this line
    def command_slime(self, state, slime, turn):
        # Find a list of plants, friends, and enemies. Also find the nearest of each
        self.find_stuff(state, slime)

        # Determine enemy and friend powers
        target = 0
        friend_power=0
        enemy_power = 0

        for friend in self.friends:
            friend_power += friend['level']

        if friend_power > 30:
            self.merge_time = True
            print('merge_time')
        elif friend_power < 20:
            self.merge_time = False
        
        for enemy in self.enemies:
            enemy_power += enemy['level']

        # Check if level is high and health is low
        if slime['current_hp'] <= 30:
            if slime['level'] >= 8:
                return Commands.SPLIT

        # check each direction for a slime then a plant, if a slime is found check if it is on our team
        bite_option = [Commands.BITELEFT, Commands.BITERIGHT, Commands.BITEUP, Commands.BITEDOWN]
        dx = [slime['x']-1, slime['x']+1, slime['x'], slime['x']]
        dy = [slime['y'], slime['y'], slime['y']+1, slime['y']-1]
        
        # check for ally slimes to merge with
        for i in range(4):
            if self.valid_coord(state, dx[i], dy[i]) and state[dx[i]][dy[i]] is not None:
                if state[dx[i]][dy[i]]['type'] == 'SLIME':
                    if state[dx[i]][dy[i]]['player_id'] == slime['player_id'] and self.merge_time:
                        print('Merge')
                        return Commands.MERGE

        # check for enemy slimes to bite
        for i in range(4):
            if self.valid_coord(state, dx[i], dy[i]) and state[dx[i]][dy[i]] is not None:
                if state[dx[i]][dy[i]]['type'] == 'SLIME':
                    if state[dx[i]][dy[i]]['player_id'] != slime['player_id']:
                        return bite_option[i]

        # check for plants to bite
        for i in range(4):
            if self.valid_coord(state, dx[i], dy[i]) and state[dx[i]][dy[i]] is not None:
                if state[dx[i]][dy[i]]['type'] == 'PLANT':
                    return bite_option[i]
        
        # Decide if its time to split
        if len(self.friends) < 6 and not self.merge_time:
            if slime['level'] >= 4:
                return Commands.SPLIT

        # Determine target
        if self.merge_time and slime['level'] < 12:
            target = self.nearest_friend
        elif slime['level'] >= 12:
            target = self.nearest_enemy
        elif len(self.plants) >= 2:
            target = self.nearest_plant
        else:
            target = self.nearest_friend

        command_call = self.a_star(target, slime, state, self.valid_coord)

        return command_call
