import arcade
import random

class Plant(arcade.Sprite):
    def __init__(self, id, config):
        super().__init__(config['plants']['filename'],
                         config['plants'].getfloat('sprite_scaling'))
        self.screen_width = config['screen'].getint('width')
        self.screen_height = config['screen'].getint('height')
        self.id = id
        self.level = 1.0
        # start at random valid location
        self.center_x = random.randrange(self.screen_width)
        self.center_y = random.randrange(self.screen_height)
        # random vector
        self.change_x = random.randrange(-3, 4)
        self.change_y = random.randrange(-3, 4)

    def update(self):
        # Move the plant
        self.center_x += self.change_x
        self.center_y += self.change_y

        # If we are out-of-bounds, then 'bounce'
        if self.left < 0:
            self.change_x *= -1

        if self.right > self.screen_width:
            self.change_x *= -1

        if self.bottom < 0:
            self.change_y *= -1

        if self.top > self.screen_height:
            self.change_y *= -1

    def level_up(self):
        print("plant", self.id, "leveled up!")
        self.level += 1
        # change size as level changes
        self.width += (self.level / 10)
        self.height += (self.level / 10)
        print(self.scale)