from models.player_base import PlayerBase
from models.commands import Commands
from models.slime import Slime

class Player(PlayerBase):
    # example player AI
    def __init__(self, player_id):
        self.id = player_id
        self.direction_x = 1
        self.move_command = Commands.RIGHT
        self.bite_command = Commands.BITERIGHT
        self.slimes = []

    def find_slimes(self, matrix):
        self.slimes = []
        for x in range(len(matrix)):
            for y in range(len(matrix[x])):
                gamepiece = matrix[x][y]
                if type(gamepiece) is Slime and gamepiece.player == self.id:
                    self.slimes.append(gamepiece)

    def command_slime(self, map, slime, turn):
        self.find_slimes(map.get_matrix())

        # if len(self.slimes) > 0 and slime.id == self.slimes[0].id:
        #     print("Controlling our original slime!")
        # else:
        #     print("Controlling some other dumb slime!")

        if slime.level >= 3:
            return Commands.SPLIT

        # determine if the slime is on the side of the map
        if slime.x == 0:
            slime.bool_1 = False
        elif slime.x == map.columns-1:
            slime.bool_1 = True

        # determine if the slime should go up or down when changing rows
        if slime.y == 0:
            slime.bool_2 = False
        elif slime.y == map.rows-1:
            slime.bool_2 = True

        # determine if the slime should change rows
        # up
        if slime.bool_3 and not slime.bool_2:
            slime.bool_3 = False
            # bite occupied square, otherwise move into it
            if not map.is_cell_empty(slime.x, slime.y+1):
                return Commands.BITEUP
            else:
                return Commands.UP

        # down
        elif slime.bool_3 and slime.bool_2:
            slime.bool_3 = False
            if not map.is_cell_empty(slime.x, slime.y-1):
                return Commands.BITEDOWN
            else:
                return Commands.DOWN
            
        # move down the row
        if not slime.bool_1:
            self.direction_x = 1
            self.move_command = Commands.RIGHT
            self.bite_command = Commands.BITERIGHT
            slime.bool_3 = True

        elif slime.bool_1:
            self.direction_x = -1
            self.move_command = Commands.LEFT
            self.bite_command = Commands.BITELEFT
            slime.bool_3 = True

        # bite occupied square, otherwise move into it
        if not map.is_cell_empty(slime.x+self.direction_x, slime.y):
            return self.bite_command
        else:
            return self.move_command
        
