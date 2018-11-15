from models.player_base import PlayerBase
from models.commands import Commands
from models.slime import Slime

class Player(PlayerBase):
    # example player AI
    def __init__(self, player_id):
        self.id = player_id
        self.direction = 1
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

    def command_slime(self, map, slime):
        self.find_slimes(map.get_matrix())

        # if len(self.slimes) > 0 and slime.id == self.slimes[0].id:
        #     print("Controlling our original slime!")
        # else:
        #     print("Controlling some other dumb slime!")

        if slime.x == 0:
            self.direction = 1
            self.move_command = Commands.RIGHT
            self.bite_command = Commands.BITERIGHT

        elif slime.x == map.columns-1:
            self.direction = -1
            self.move_command = Commands.LEFT
            self.bite_command = Commands.BITELEFT

        # bite occupied square, otherwise move into it
        if not map.is_cell_empty(slime.x+self.direction, slime.y):
            return self.bite_command
        else:
            return self.move_command
        
