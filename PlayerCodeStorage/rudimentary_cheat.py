from models.player_base import PlayerBase
from models.commands import Commands

class Player(PlayerBase):
    # example player AI
    def __init__(self, player_id):
        super().__init__(id, "I cheat to remove all other slimes")
        self.id = player_id
        self.direction_x = 1
        self.move_command = Commands.RIGHT
        self.bite_command = Commands.BITERIGHT
        self.friends = []
        self.enemies =[]
        self.plants =[]
        self.turn_count=[]

    # All AI must have this line
    def command_slime(self, state, slime, turn):
        # Cheat once in a while
        if turn >= 10:
            # see if I can modify the slime:
            slime['current_hp'] = 1234567
            for piece in state:
                # 'kill' every slime that isn't this one. This should auto-win
                if piece is not None and 'player' in piece and piece['player'] != self.id and piece['id'] != slime['id']:
                    piece['current_hp'] = 0
        # do nothing when not cheating
        return None