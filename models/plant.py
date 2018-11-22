import random
import arcade
from models.gamepiece import Gamepiece

class Plant(Gamepiece):
    def __init__(self, config):
        super().__init__(config['filename1'],
                         config.getfloat('sprite_scaling'),
                         config)
        self.level = 1
        self.max_hp = config.getint('max_hp')
        self.current_hp = self.max_hp
        self.max_level = config.getint('max_level')
        self.hp_increment = config.getint('hp_increment')

    def update(self):
        self.level_up()

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

            if self.level >= int(self.max_level * 3 / 4):
                self.texture = arcade.draw_commands.load_texture(self.conf.get('filename2'), scale = self.scale)

            # Change max hp on level up
            self.max_hp += self.hp_increment

            # Add hp on level up, not exceeding max
            self.current_hp = min(self.current_hp + self.max_hp//2, self.max_hp)

    def reset_level(self):
        self.level = 1
        self.max_hp = self.conf.getint('max_hp')
        self.current_hp = self.max_hp
        self.texture = arcade.draw_commands.load_texture(self.conf.get('filename1'), scale = self.scale)

    def can_seed(self):
        return self.level == self.max_level

