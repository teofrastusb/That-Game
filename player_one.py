from models.player_base import PlayerBase
from models.commands import Commands

# All codes could use the same class name
class Player(PlayerBase):
    # example player AI
    def __init__(self):
        self.direction = 1
        self.move_command = Commands.RIGHT
        self.bite_command = Commands.BITERIGHT

    def command_slime(self, map, slime):
        if slime.x == 0:
            self.direction = 1
            self.move_command = Commands.RIGHT
            self.bite_command = Commands.BITERIGHT

        elif slime.x == map.columns*2-1:
            self.direction = -1
            self.move_command = Commands.LEFT
            self.bite_command = Commands.BITELEFT

        target = map.matrix[slime.x+self.direction][slime.y]
        #print(target)
        # check for biteable
        
        if not(target == 0):

            # check for same team
            if not(hasattr(target,'player') and target.player == slime.player):
                return self.bite_command

        else:
            return self.move_command
        
