from models.player_base import PlayerBase

class PlayerOne(PlayerBase):
    # example player AI
    def command_slime(self, map, slime):
        # reaaaaal dumb AI
        return list(self.commands)[0]
