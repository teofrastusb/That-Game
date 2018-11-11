import arcade
import random

class Plant(arcade.Sprite):
    def __init__(self, id, config, map):
        super().__init__(config['plants']['filename'],
                         config['plants'].getfloat('sprite_scaling'))
        self.id = id
        self.level = 1.0
        self.map = map

    def update(self):
        # nothin to do...yet
        pass

    def set_coord(self, x, y):
        self.x = x
        self.y = y
        # display
        self.set_position(self.map.center_x(x), self.map.center_y(y))

    def level_up(self):
        print("plant", self.id, "leveled up!")
        self.level += 1
        # change size as level changes
        self.width += (self.level / 10)
        self.height += (self.level / 10)
        print(self.scale)