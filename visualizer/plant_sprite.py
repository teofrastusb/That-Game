import random
import arcade

class PlantSprite(arcade.Sprite):
    def __init__(self, config, id):
        self.filename = config.get('filename1')
        super().__init__(self.filename, config.getfloat('sprite_scaling'))
        self.id = id
        self.conf = config

    def update_texture(self, piece):
        if piece['level'] >= int(self.conf.getint('max_level') * 3 / 4):
            filename = self.conf.get('filename2')
        else:
            filename = self.conf.get('filename1')
        # only load texture on changes
        if self.filename != filename:
            self.filename = filename
            self.texture = arcade.draw_commands.load_texture(filename, scale = self.conf.getfloat('sprite_scaling'))
