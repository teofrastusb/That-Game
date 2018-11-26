import arcade

class SlimeSprite(arcade.Sprite):
    def __init__(self, config, id):
        self.filename = config.get('player_one_basic')
        super().__init__(self.filename, config.getfloat('sprite_scaling'))
        self.id = id
        self.conf = config

    def update_texture(self, piece):
        """Update the slimes sprites based on player and level."""
        if piece['player'] == 1:
            if piece['level'] < self.conf.getint('max_level') - 2:
                filename = self.conf.get('player_one_basic')
            else:
                filename = self.conf.get('player_one_king')
        else:
            if piece['level'] < self.conf.getint('max_level') - 2:
                filename = self.conf.get('player_two_basic')
            else:
                filename = self.conf.get('player_two_king')
        # only load texture on changes
        if self.filename != filename:
            self.filename = filename
            self.texture = arcade.draw_commands.load_texture(filename, scale = self.conf.getfloat('sprite_scaling'))