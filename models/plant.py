import arcade
import random

class Plant(arcade.Sprite):
    def __init__(self, id, config, map):
        super().__init__(config['plants']['filename'],
                         config['plants'].getfloat('sprite_scaling'))
        self.id = id
        self.level = 1
        self.map = map
        self.max_hp = config['plants'].getint('max_hp')
        self.hp = self.max_hp

    def update(self):
        # nothin to do...yet
        pass

    def set_coord(self, x, y):
        self.x = x
        self.y = y
        # display
        self.set_position(self.map.center_x(x), self.map.center_y(y))

    def level_up(self):
        print("plant", self.id, "leveled up to",self.level,"!")
        self.level += 1

        # Change max hp on level up
        self.max_hp += self.max_hp//2

        # Add hp on level up
        self.hp += self.max_hp//2
        if self.hp >= self.max_hp:
            self.hp = self.max_hp


