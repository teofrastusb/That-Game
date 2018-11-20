from models.gamepiece import Gamepiece

class Rock(Gamepiece):
    def __init__(self, config, map):
        super().__init__(config['rocks']['filename1'],
                         config['rocks'].getfloat('sprite_scaling'),
                         config,
                         map)