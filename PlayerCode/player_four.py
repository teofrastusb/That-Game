from models.player_base import PlayerBase
from models.commands import Commands
import random
from models.slime import Slime
from models.plant import Plant
from models.rock import Rock

# All codes could use the same class name
class Player(PlayerBase):
    # example player AI
    def __init__(self, player_id):
        self.id = player_id
        self.direction_x = 1
        self.move_command = Commands.RIGHT
        self.bite_command = Commands.BITERIGHT
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
                if type(gamepiece) is Slime and gamepiece.player == self.id:
                    self.friends.append(gamepiece)
                if type(gamepiece) is Slime and gamepiece.player != self.id:
                    self.enemies.append(gamepiece)
                if type(gamepiece) is Plant:
                    self.plants.append(gamepiece)
    
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

        if len(self.friends) <= 5:
            if slime.level >= 4:
                return Commands.SPLIT

        # Move with a purpose
        nearest_plant= 0
        nearest_plant_distance = 0
        for palnt in self.plants:
            distance = int(((self.x-palnt.x)**2 + (self.y-plant.y)**2)**(1/2))
            if nearest_plant_distance < distance:
                nearest_plant = palnt

        command_options = [Commands.LEFT,Commands.RIGHT,Commands.UP,Commands.DOWN]
        option = random.randint(0,3)
        command_call = command_options[option]
        return command_call
