from models.player_base import PlayerBase

class PlayerTwo(PlayerBase):
    # example player AI
    def command_slime(self, map, slime):
        # just do default
        return super().command_slime(map, slime)
