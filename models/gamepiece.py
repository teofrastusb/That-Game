import arcade
import uuid

class Gamepiece(arcade.Sprite):
    def __init__(self, filename, scale, config, player = 0):
        super().__init__(filename, scale)
        self.id = uuid.uuid4()
        self.player = player
        self.x = None
        self.y = None
        self.conf = config
        self.scale = scale