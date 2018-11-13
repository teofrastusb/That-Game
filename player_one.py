from models.player_base import PlayerBase
from models.commands import Commands

# All codes could use the same class name
class Player(PlayerBase):
    # example player AI
    def command_slime(self, map, slime):
        # reaaaaal dumb AI
        return Commands.RIGHT
