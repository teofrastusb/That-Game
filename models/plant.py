import arcade
import random

class Plant(arcade.Sprite):
    def __init__(self, id, config, map):
        super().__init__(config['plants']['filename'],
                         config['plants'].getfloat('sprite_scaling'))
        self.id = id
        self.level = 1.0
        self.map = map
        # start at random valid location
        rand_x = random.randint(1, map.row_count() / 2)
        rand_y = random.randint(1, map.column_count())
        self.set_position(rand_x * map.step_x(), rand_y * map.step_y())

    def update(self):
        # nothin to do...yet
        pass

    def set_map(self, map):
        self.map = map

    def level_up(self):
        print("plant", self.id, "leveled up!")
        self.level += 1
        # change size as level changes
        self.width += (self.level / 10)
        self.height += (self.level / 10)
        print(self.scale)