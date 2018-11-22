from models.gamepiece import Gamepiece

class Rock(Gamepiece):
    def __init__(self, config):
        super().__init__(config['filename1'],
                         config.getfloat('sprite_scaling'),
                         config)

    def __dict__(self):
        return { 'type': 'ROCK', 'x': self.x, 'y': self.y }