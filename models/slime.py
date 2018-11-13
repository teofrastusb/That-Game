import arcade

class Slime(arcade.Sprite):
    def __init__(self, id, config, map):
        super().__init__(config['slimes']['filename'],
                         config['slimes'].getfloat('sprite_scaling'))
        self.id = id
        self.row = 0
        self.column = 0
        self.map = map
        self.level = 1
        self.xp = 1
        self.max_level = config['slimes'].getint('max_level')
        self.current_hp = config['slimes'].getint('max_hp')
        self.max_hp = config['slimes'].getint('max_hp')
        self.hp_increment = self.max_hp
        self.attack = config['slimes'].getint('attack')
        self.attack_increment = self.attack

    def update(self):
        # nothin to do...yet
        self.level_up()

    def set_coord(self, x, y):
        self.x = x
        self.y = y
        self.map.update_cell(self, x, y)
        # display
        self.set_position(self.map.center_x(x), self.map.center_y(y))

    def level_up(self):
        # Save current level
        starting_level = self.level

        # Update level based on xp
        self.level = int((-0.001*self.xp+0.185)*self.xp+1.9)

        # Check if the slime level is at or above maximum
        if self.level >= self.max_level:
            self.level = self.max_level

        # If the slime leveled up do the following
        if self.level > starting_level:

            # Change max hp on level up
            self.max_hp += self.hp_increment

            # Add hp on level up
            self.current_hp += self.hp_increment
            if self.current_hp >= self.max_hp:
                self.current_hp = self.max_hp

            # Add attack on level up
            self.attack += self.attack_increment
