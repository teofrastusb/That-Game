import arcade
import random

class Rock(arcade.Sprite):
    def __init__(self, id, config, map):
        super().__init__(config['rocks']['filename1'],
                         config['rocks'].getfloat('sprite_scaling'))
        self.id = id
        self.x = None
        self.y = None
        self.map = map
        self.conf = config

    def update(self):
        # rock does nothing
        pass

    def set_coord(self, x, y):
        if self.x is not None and self.y is not None:
            self.map.clear_cell(self.x, self.y)
        self.x = x
        self.y = y
        self.map.update_cell(self, x, y)
        # display
        self.set_position(self.map.center_x(x), self.map.center_y(y))

   