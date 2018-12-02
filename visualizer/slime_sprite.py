import arcade
from PIL import Image

class SlimeSprite(arcade.Sprite):
    def __init__(self, config, piece):
        self.conf = config
        self.filename = self.choose_texture(piece)
        self.id = piece['id']
        im = Image.open(config['Slime'].get('player_one_basic'))
        width, height = im.size
        self.scale_adj = (config['screen'].getfloat('width')/config['screen'].getfloat('columns'))/(width)*1.2
        super().__init__(self.filename, self.scale_adj)

    def choose_texture(self, piece):
        if piece['player'] == 1:
            if piece['level'] < 10:
                filename = self.conf['Slime'].get('player_one_basic')
            else:
                filename = self.conf['Slime'].get('player_one_king')
        else:
            if piece['level'] < 10:
                filename = self.conf['Slime'].get('player_two_basic')
            else:
                filename = self.conf['Slime'].get('player_two_king')
        return filename

    def update_texture(self, piece):
        """Update the slimes sprites based on player and level."""
        filename = self.choose_texture(piece)
        # only load texture on changes
        if self.filename != filename:
            self.filename = filename
            self.texture = arcade.draw_commands.load_texture(filename, scale = self.scale_adj)