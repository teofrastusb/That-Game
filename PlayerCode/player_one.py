from models.player_base import PlayerBase
from models.commands import Commands
from models.slime import Slime

class SlimeState():
    def __init__(self):
        self.bool_1 = False
        self.bool_2 = False
        self.bool_3 = False

class Player(PlayerBase):
    # example player AI
    def __init__(self, id):
        super().__init__(id, "The Fighting Mongooses")
        self.direction_x = 1
        self.move_command = Commands.RIGHT
        self.bite_command = Commands.BITERIGHT
        self.slimes = {}

    def get_state(self, slime_id):
        if slime_id not in self.slimes:
            self.slimes[slime_id] = SlimeState()
        return self.slimes[slime_id]

    def command_slime(self, map, slime, turn):
        state = self.get_state(slime.id)
        
        if slime.level >= 3:
            return Commands.SPLIT

        # determine if the slime is on the side of the map
        if slime.x == 0:
            state.bool_1 = False
        elif slime.x == map.columns-1:
            state.bool_1 = True

        # determine if the slime should go up or down when changing rows
        if slime.y == 0:
            state.bool_2 = False
        elif slime.y == map.rows-1:
            state.bool_2 = True

        # determine if the slime should change rows
        # up
        if state.bool_3 and not state.bool_2:
            state.bool_3 = False
            # bite occupied square, otherwise move into it
            if not map.is_cell_empty(slime.x, slime.y+1):
                return Commands.BITEUP
            else:
                return Commands.UP

        # down
        elif state.bool_3 and state.bool_2:
            state.bool_3 = False
            if not map.is_cell_empty(slime.x, slime.y-1):
                return Commands.BITEDOWN
            else:
                return Commands.DOWN
            
        # move down the row
        if not state.bool_1:
            self.direction_x = 1
            self.move_command = Commands.RIGHT
            self.bite_command = Commands.BITERIGHT
            state.bool_3 = True

        elif state.bool_1:
            self.direction_x = -1
            self.move_command = Commands.LEFT
            self.bite_command = Commands.BITELEFT
            state.bool_3 = True

        # bite occupied square, otherwise move into it
        if not map.is_cell_empty(slime.x+self.direction_x, slime.y):
            return self.bite_command
        else:
            return self.move_command
        
