import arcade
import random

class Plant(arcade.Sprite):
    def __init__(self, id, config, map):
        super().__init__(config['plants']['filename'],
                         config['plants'].getfloat('sprite_scaling'))
        self.id = id
        self.level = 1
        self.map = map
        self.conf = config
        self.max_hp = config['plants'].getint('max_hp')
        self.current_hp = self.max_hp
        self.max_level = config['plants'].getint('max_level')
        self.hp_increment = self.max_level
        self.seed = False

    def update(self):
        self.level_up()

    def set_coord(self, x, y):
        self.x = x
        self.y = y
        self.map.update_cell(self, x, y)
        # display
        self.set_position(self.map.center_x(x), self.map.center_y(y))

    def level_up(self):
        # Check if the plant levels up
        do_level_up = 0

        level_up_chance = random.randint(0,self.conf['plants'].getint('level_up_chance_one'))
        if level_up_chance == 0:
            level_up_chance = random.randint(0,self.max_level + self.conf['plants'].getint('level_up_chance_two'))
            if level_up_chance > self.level and self.level < self.max_level:
                do_level_up = 1

        # If the plant levels up do the following
        if do_level_up:
            self.level += 1

            # Change max hp on level up
            self.max_hp += self.hp_increment

            # Add hp on level up, not exceeding max
            self.current_htp = min(self.current_hp + self.max_hp//2, self.max_hp)

            # Check if the level is now max level
            if self.level == self.max_level:
                self.seed = True

