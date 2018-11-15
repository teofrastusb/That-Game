import arcade
import random
import uuid
from models.plant import Plant

class Sprite_man():
    def __init__(self, map, config, all_sprites_list):
        self.all_sprites_list = all_sprites_list
        self.map = map
        self.conf = config

    def place_plant(self, x, y):
        plant = Plant(uuid.uuid4(), self.conf, self.map)
        plant.set_coord(x, y)
        self.all_sprites_list.append(plant)

    def check_for_dead(self):
        for gamepiece in self.all_sprites_list:
            if gamepiece.current_hp <= 0:
                arcade.sprite.Sprite.kill(gamepiece) 
                self.map.clear_cell(gamepiece.x,gamepiece.y)

    def spread_seeds(self):
        for plant in self.all_sprites_list:
            if type(plant) is Plant and plant.can_seed():
                empty_adjacent_cells = self.map.adjacent_empty_cells(plant.x, plant.y)

                # can't seed if there are no available cells
                if len(empty_adjacent_cells) == 0:
                    continue

                x, y = random.choice(empty_adjacent_cells)
                self.place_plant(x, y)
                plant.reset_level()
