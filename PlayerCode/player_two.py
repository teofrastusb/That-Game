from models.player_base import PlayerBase
from models.commands import Commands
import random
from models.slime import Slime
from models.plant import Plant

# All codes could use the same class name
class Player(PlayerBase):
    # example player AI
    def __init__(self, id):
        super().__init__(id, "player_two")
        self.direction_x = 1
        self.move_command = Commands.RIGHT
        self.bite_command = Commands.BITERIGHT
        self.freinds = []
        self.enemies =[]
        self.plants =[]

    def find_stuff(self, matrix):
        self.freinds = []
        self.enemies =[]
        self.plants =[]
        for x in range(len(matrix)):
            for y in range(len(matrix[x])):
                gamepiece = matrix[x][y]
                if type(gamepiece) is Slime and gamepiece.player == self.id:
                    self.freinds.append(gamepiece)
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
        if slime.x != 0 and map.matrix[slime.x-1][slime.y] != None:
            if type(map.matrix[slime.x-1][slime.y]) is Plant:
                return Commands.BITELEFT
            elif map.matrix[slime.x-1][slime.y].player != slime.player:
                return Commands.BITELEFT
        elif slime.x != map.columns-1 and map.matrix[slime.x+1][slime.y] != None:
            if not hasattr(map.matrix[slime.x+1][slime.y],'player'):
                return Commands.BITERIGHT
            elif map.matrix[slime.x+1][slime.y].player != slime.player:
                return Commands.BITERIGHT
        elif slime.y != 0 and map.matrix[slime.x][slime.y-1] != None:
            if not hasattr(map.matrix[slime.x][slime.y-1],'player'):
                return Commands.BITEDOWN
            elif map.matrix[slime.x][slime.y-1].player != slime.player:
                return Commands.BITEDOWN
        elif slime.y != map.rows-1 and map.matrix[slime.x][slime.y+1] != None:
            if not hasattr(map.matrix[slime.x][slime.y+1],'player'):
                return Commands.BITEUP
            elif map.matrix[slime.x][slime.y+1].player != slime.player:
                return Commands.BITEUP

        if slime.level >= 5:
            return Commands.SPLIT

        # Move randomly
        command_options = [Commands.LEFT,Commands.RIGHT,Commands.UP,Commands.DOWN]
        option = random.randint(0,3)
        command_call = command_options[option]
        return command_call
