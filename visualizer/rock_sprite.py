import arcade
from PIL import Image

class RockSprite(arcade.Sprite):
    def __init__(self, config, id):
        im = Image.open(config['Rock'].get('filename1'))
        width, height = im.size
        scale_adj = (config['screen'].getfloat('width')/config['screen'].getfloat('columns'))/(width)*1.1
        super().__init__(config['Rock'].get('filename1'), scale_adj)
        self.id = id