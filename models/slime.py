import arcade

class Slime(arcade.Sprite):
    def __init__(self, id, config, map):
        super().__init__(config['slimes']['filename'],
                         config['slimes'].getfloat('sprite_scaling'))
        self.id = id
        self.row = 0
        self.column = 0
        self.map = map
        self.xp = 0
        self.current_hp = config['slimes'].getint('max_hp')
        self.max_hp = config['slimes'].getint('max_hp')

    def update(self):
        # nothin to do...yet
        pass

    def set_coord(self, x, y):
        self.x = x
        self.y = y
        self.map.update_cell(self, x, y)
        # display
        self.set_position(self.map.center_x(x), self.map.center_y(y))