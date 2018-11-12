from models.player_base import PlayerBase

# All codes could use the same class name
class Player(PlayerBase):
    # example player AI
    def command_slime(self, map, slime):
        # just do default
        return super().command_slime(map, slime)
