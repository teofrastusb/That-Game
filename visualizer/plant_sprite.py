import random
import arcade
from PIL import Image

class PlantSprite(arcade.Sprite):
    def __init__(self, config, id):
        self.conf = config
        self.filename = self.conf['Plant'].get('filename1')
        self.id = id
        im = Image.open(config['Plant'].get('filename1'))
        width, height = im.size
        self.scale_adj = (config['screen'].getfloat('width')/config['screen'].getfloat('columns'))/(width)*1.2
        super().__init__(self.filename, self.scale_adj)     

    def update_texture(self, piece):
        if piece['level'] >= int(self.conf['Plant'].getint('max_level') * 3 / 4):
            filename = self.conf['Plant'].get('filename2')
        else:
            filename = self.conf['Plant'].get('filename1')
        # only load texture on changes
        if self.filename != filename:
            self.filename = filename
            self.texture = arcade.draw_commands.load_texture(filename, scale = self.scale_adj)
