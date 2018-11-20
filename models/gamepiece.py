import arcade
import uuid

class Gamepiece(arcade.Sprite):
    def __init__(self, filename, scaling, config, map, player = 0):
        super().__init__(filename, scaling)
        self.id = uuid.uuid4()
        self.player = player
        self.x = None
        self.y = None
        self.map = map
        self.conf = config

    def set_coord(self, x, y):
        if self.x is not None and self.y is not None:
            self.map.clear_cell(self.x, self.y)
        self.x = x
        self.y = y
        self.map.update_cell(self, x, y)
        # display
        self.set_position(self.map.center_x(x), self.map.center_y(y))