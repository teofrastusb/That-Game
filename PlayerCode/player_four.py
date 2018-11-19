from models.player_base import PlayerBase
from models.commands import Commands
from models.slime import Slime
from models.plant import Plant
from models.rock import Rock
import random

# All codes could use the same class name
class Player(PlayerBase):
    # example player AI
    def __init__(self, player_id):
        super().__init__(id, "6 pack attack")
        self.id = player_id
        self.direction_x = 1
        self.move_command = Commands.RIGHT
        self.bite_command = Commands.BITERIGHT
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
                if type(gamepiece) is Slime and gamepiece.player == self.id:
                    self.friends.append(gamepiece)
                if type(gamepiece) is Slime and gamepiece.player != self.id:
                    self.enemies.append(gamepiece)
                if type(gamepiece) is Plant:
                    self.plants.append(gamepiece)

    # All AI must have this line
    def a_star(self, target, slime):
        if target != 0:
            if slime.x > target.x:
                return Commands.LEFT
            elif slime.x < target.x:
                return Commands.RIGHT
            elif slime.y > target.y:
                return Commands.DOWN
            elif slime.y < target.y:
                return Commands.UP

    # All AI must have this line
    def command_slime(self, map, slime, turn):
        self.find_stuff(map.get_matrix())
        
        # if turn == 1:
        #     return Commands.MERGE

        # check each direction for a plant then a slime, if a slime is found check if it is on our team
        bite_option = [Commands.BITELEFT, Commands.BITERIGHT, Commands.BITEUP, Commands.BITEDOWN]
        dx = [slime.x-1, slime.x+1, slime.x, slime.x]
        dy = [slime.y, slime.y, slime.y+1, slime.y-1]
        
        for i in range(4):
            if map.valid_coord(dx[i], dy[i]) and map.matrix[dx[i]][dy[i]] != None:
                if type(map.matrix[dx[i]][dy[i]]) is Plant:
                    return bite_option[i]
                elif type(map.matrix[dx[i]][dy[i]]) is not Rock:
                    if map.matrix[dx[i]][dy[i]].player != slime.player:
                        return bite_option[i]

        if len(self.friends) < 6:
            if slime.level >= 4:
                return Commands.SPLIT

        # Move with a purpose
        # Find nearest plant
        nearest_plant= 0
        plants_checked= 0
        nearest_plant_distance = 1000
        for plant in self.plants:
            plants_checked += 1
            distance = abs(slime.x-plant.x)+abs(slime.y-plant.y)
            if nearest_plant_distance > distance:
                nearest_plant = plant

        # Find nearest enemy
        nearest_enemy= 0
        nearest_enemy_distance = 0
        for enemy in self.enemies:
            distance = int(((slime.x-enemy.x)**2 + (slime.y-enemy.y)**2)**(1/2))
            if nearest_enemy_distance < distance:
                nearest_enemy = enemy

        # Determine if there are enough friends to attack
        target = 0

        friend_power=0
        for friend in self.friends:
            friend_power += friend.level

        if friend_power < 30 and len(self.plants) > 0:
            target = nearest_plant
        else:
            target = nearest_enemy

        command_call = self.a_star(target, slime)

        return command_call
