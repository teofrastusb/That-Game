from models.player_base import PlayerBase

# All codes could use the same class name
class Player(PlayerBase):
    # example player AI
    def command_slime(self, map, slime):
        # reaaaaal dumb AI
        return list(self.commands)[0]
