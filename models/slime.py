import arcade
from models.gamepiece import Gamepiece

class Slime(Gamepiece):
    def __init__(self, config, map, player):
        super().__init__(config.get('player_one_basic'),
                         config.getfloat('sprite_scaling'),
                         config,
                         map,
                         player)
        self.level = 1
        self.xp = 1
        self.max_level = config.getint('max_level')

        self.hp_exponent = config.getfloat('hp_exponent')
        self.hp_base = config.getint('hp_base')
        self.current_hp =config.getint('hp_base')

        self.attack_exponent = config.getfloat('attack_exponent')
        self.attack_base = config.getint('attack_base')
        self.attack =config.getint('attack_base')

        self.min_split_level = config.getint('min_split_level')
        self.ready_to_merge = False

    def update(self):
        self.level_check()
        self.update_texture()

    def update_texture(self):
        """Update the slimes sprites based on player and level."""
        if self.player == 1:
            if self.level < self.max_level - 2:
                filename = self.conf.get('player_one_basic')
            else:
                filename = self.conf.get('player_one_king')
        else:
            if self.level < self.max_level - 2:
                filename = self.conf.get('player_two_basic')
            else:
                filename = self.conf.get('player_two_king')
        self.texture = arcade.draw_commands.load_texture(filename, scale = self.scale)

    def split(self):
        self.xp = self.xp // 3

    def level_check(self):
        # Save current level
        starting_level = self.level

        # Update level based on xp
        self.level = int(1.77*self.xp**0.331+1)

        # Check if the slime level is at or above maximum
        if self.level >= self.max_level:
            self.level = self.max_level

        # Update attack based on level
        self.attack = self.level**self.attack_exponent+self.attack_base

        # Update max hp based on level
        self.max_hp = self.level**self.hp_exponent+self.hp_base

        # Add hp on level up
        if starting_level < self.level:
            self.max_hp = self.level**self.hp_exponent+self.hp_base
            if self.max_hp>(starting_level**self.hp_exponent+self.hp_base):
                self.current_hp += (self.max_hp-(starting_level**self.hp_exponent+self.hp_base))
            # make sure current hp isn't above max hp
                if self.current_hp >= self.max_hp:
                    self.current_hp = self.max_hp
