import random
import arcade
from models.gamepiece import Gamepiece

class Plant(Gamepiece):
    def __init__(self, config, map):
        super().__init__(config['filename1'],
                         config.getfloat('sprite_scaling'),
                         config,
                         map)
        self.level = 1
        self.max_hp = config.getint('max_hp')
        self.current_hp = self.max_hp
        self.max_level = config.getint('max_level')
        self.hp_increment = self.max_level

    def update(self):
        self.level_up()

    def set_coord(self, x, y):
        if self.x is not None and self.y is not None:
            self.map.clear_cell(self.x, self.y)
        self.x = x
        self.y = y
        self.map.update_cell(self, x, y)
        # display
        self.set_position(self.map.center_x(x), self.map.center_y(y))

    def level_up(self):
        # Check if the plant levels up
        do_level_up = 0

        level_up_chance = random.randint(0,self.conf.getint('level_up_chance_one'))
        if level_up_chance == 0:
            level_up_chance = random.randint(0,self.max_level + self.conf.getint('level_up_chance_two'))
            if level_up_chance > self.level and self.level < self.max_level:
                do_level_up = 1

        # If the plant levels up do the following
        if do_level_up:
            self.level += 1

            if self.level >= int(self.max_level*3/4):
                self.texture=arcade.draw_commands.load_texture(self.conf.get('filename2'),
                scale=self.conf.getfloat('sprite_scaling'))

                # Change image based on level
            if self.level >= self.max_level//2:
                # TODO change sprite image to the next image
                arcade.Sprite(self.conf['filename2'],
                                self.conf.getfloat('sprite_scaling'))

            # Change max hp on level up
            self.max_hp += self.hp_increment

            # Add hp on level up, not exceeding max
            self.current_htp = min(self.current_hp + self.max_hp//2, self.max_hp)

    def reset_level(self):
        self.level = 1
        self.max_hp = self.conf.getint('max_hp')
        self.current_hp = self.max_hp
        self.texture=arcade.draw_commands.load_texture(self.conf.get('filename1'),
                scale=self.conf.getfloat('sprite_scaling'))

    def can_seed(self):
        return self.level == self.max_level

