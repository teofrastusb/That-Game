import arcade
import random

class Plant(arcade.Sprite):
    def __init__(self, id, config, map):
        super().__init__(config['plants']['filename'],
                         config['plants'].getfloat('sprite_scaling'))
        self.id = id
        self.level = 1
        self.map = map 
        # Why cant I put these next two lines into the init method instead of the super init method 
        self.max_hp = config['plants'].getint('max_hp')
        self.hp = self.max_hp
        self.max_level = config['plants'].getint('max_level')

    def update(self):
        # nothin to do...yet
        pass

    def set_coord(self, x, y):
        self.x = x
        self.y = y
        # display
        self.set_position(self.map.center_x(x), self.map.center_y(y))

    def level_up(self):
        # Check if the plant levels up
        do_level_up = 0

        level_up_chance = random.randint(0,self.max_level)
        if level_up_chance > self.level:
            level_up_chance = random.randint(0,self.max_level)
            if level_up_chance > self.level:
                level_up_chance = random.randint(0,self.max_level)
                if level_up_chance > self.level:
                    do_level_up = 1

        # If the plant levels up do the following
        if do_level_up:
            self.level += 1

            print("plant", self.id, "leveled up to",self.level,"!")

            # Change max hp on level up
            self.max_hp += self.max_hp//2

            # Add hp on level up
            self.hp += self.max_hp//2
            if self.hp >= self.max_hp:
                self.hp = self.max_hp

    def seed(self):
        # Check if the plant is level 20
        pass


