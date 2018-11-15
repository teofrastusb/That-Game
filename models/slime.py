import arcade

class Slime(arcade.Sprite):
    def __init__(self, id, config, map, player):
        super().__init__(config['slimes']['filename'],
                         config['slimes'].getfloat('sprite_scaling'))
        self.id = id
        self.row = 0
        self.column = 0
        self.map = map
        self.level = 1
        self.xp = 1
        self.player = player
        self.max_level = config['slimes'].getint('max_level')
        self.current_hp = config['slimes'].getint('max_hp')
        self.max_hp = config['slimes'].getint('max_hp')
        self.hp_increment = config['slimes'].getint('hp_increment')
        self.attack = config['slimes'].getint('attack')
        self.attack_increment = config['slimes'].getint('attack_increment')

    def update(self):
        # Check level, then ...
        self.level_check()

    def set_coord(self, x, y):
        self.x = x
        self.y = y
        self.map.update_cell(self, x, y)
        # display
        self.set_position(self.map.center_x(x), self.map.center_y(y))

    def split(self):
        self.xp = self.xp // 2.2

    def level_check(self):
        # Save current level
        starting_level = self.level

        # Update level based on xp
        self.level = int((-0.001*self.xp+0.185)*self.xp+1.9)

        # Check if the slime level is at or above maximum
        if self.level >= self.max_level:
            self.level = self.max_level

        # Update attack based on level up
        self.attack = self.level*self.attack_increment

        # Update max hp based on level
        self.max_hp = self.level*self.hp_increment

        # Add hp on level up
        if starting_level < self.level:
            self.current_hp += self.hp_increment
            print('xp', self.xp)
            print('level', self.level)
            print('max hp', self.max_hp)
            print('current hp', self.current_hp)
        
        # make sure current hp isn't above max hp
        if self.current_hp >= self.max_hp:
            self.current_hp = self.max_hp


            