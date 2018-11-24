import arcade

class RockSprite(arcade.Sprite):
    def __init__(self, config, id):
        super().__init__(config['filename1'], config.getfloat('sprite_scaling'))
        self.id = id