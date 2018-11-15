import arcade
import random
import uuid
from models.plant import Plant

class Sprite_man():
    def __init__(self, map, config, plant_list, slimes_one, slimes_two, all_sprites_list):
        self.plant_list = plant_list
        self.slimes_one = slimes_one
        self.slimes_two = slimes_two
        self.all_sprites_list = all_sprites_list
        self.map = map
        self.conf = config

    def place_plant(self, x, y):
        plant = Plant(uuid.uuid4(), self.conf, self.map)
        plant.set_coord(x, y)
        self.plant_list.append(plant)
        self.all_sprites_list.append(plant)

    def check_for_dead(self):
        #print('Bring out your dead!')
        self.kill_list = []

        for plant in self.plant_list:
            if plant.current_hp <= 0:
                self.kill_list.append(plant)

        for slime in self.slimes_one:
            if slime.current_hp <= 0:
                self.kill_list.append(slime)

        for slime in self.slimes_two:
            if slime.current_hp <= 0:
                self.kill_list.append(slime)

        for gamepiece in self.kill_list:
            print('clearing dead')
            arcade.sprite.Sprite.kill(gamepiece) 
            self.map.clear_cell(gamepiece.x,gamepiece.y)

    def spread_seeds(self):
        for plant in self.plant_list:
            if plant.can_seed():
                empty_adjacent_cells = self.map.adjacent_empty_cells(plant.x, plant.y)

                # can't seed if there are no available cells
                if len(empty_adjacent_cells) == 0:
                    continue

                x, y = random.choice(empty_adjacent_cells)
                self.place_plant(x, y)
                plant.reset_level()
