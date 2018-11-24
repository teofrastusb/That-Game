import random
import arcade

class PlantSprite(arcade.Sprite):
    def __init__(self, config, id):
        super().__init__(config['filename1'], config.getfloat('sprite_scaling'))
        self.id = id
        self.conf = config

    def update_texture(self, piece):
        if piece['level'] >= int(self.conf.getint('max_level') * 3 / 4):
            self.texture = arcade.draw_commands.load_texture(self.conf.get('filename2'), scale = self.conf.getfloat('sprite_scaling'))
        elif piece['level'] == 1:
            self.texture = arcade.draw_commands.load_texture(self.conf.get('filename1'), scale = self.conf.getfloat('sprite_scaling'))
