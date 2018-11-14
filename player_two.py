from models.player_base import PlayerBase
from models.commands import Commands
import random

# All codes could use the same class name
class Player(PlayerBase):
    # example player AI
    def command_slime(self, map, slime):
        # just do default
        command_options = [Commands.LEFT,Commands.RIGHT,Commands.UP,Commands.DOWN]
        option = random.randint(0,3)
        command_call = command_options[option]
        return command_call
