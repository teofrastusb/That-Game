import arcade
import random
import uuid
import math
import logging
from models.plant import Plant
from models.slime import Slime
from models.rock import Rock

class Sprite_man():
    def __init__(self, map, config, all_sprites_list):
        self.all_sprites_list = all_sprites_list
        self.map = map
        self.conf = config

    def place_gamepiece(self, piece_class, x, y, player = 0):
        if piece_class is Slime:
            piece = piece_class(self.conf, self.map, player)
        else:
            piece = piece_class(self.conf, self.map)
        piece.set_coord(x, y)
        self.all_sprites_list.append(piece)

    def check_for_dead(self):
        for gamepiece in self.all_sprites_list:
            if type(gamepiece) is not Rock:
                if gamepiece.current_hp <= 0:
                    arcade.sprite.Sprite.kill(gamepiece) 
                    self.map.clear_cell(gamepiece.x,gamepiece.y)

    def check_for_merge(self):
        for gamepiece in self.all_sprites_list:
            if type(gamepiece) is Slime and gamepiece.ready_to_merge:
                for x, y in self.map.adjacent_cells(gamepiece.x, gamepiece.y):
                    neighbor = self.map.get_matrix()[x][y]
                    if neighbor is not None and type(neighbor) is Slime and neighbor.ready_to_merge and gamepiece.player == neighbor.player:
                        logging.getLogger().info('%s merged with %s', gamepiece.id, neighbor.id)
                        gamepiece.xp = math.floor(1.5 * (gamepiece.xp + neighbor.xp))
                        arcade.sprite.Sprite.kill(neighbor)
                        self.map.clear_cell(neighbor.x, neighbor.y)
                        

    def spread_seeds(self):
        for plant in self.all_sprites_list:
            if type(plant) is Plant and plant.can_seed():
                empty_adjacent_cells = self.map.adjacent_empty_cells(plant.x, plant.y)

                # can't seed if there are no available cells
                if len(empty_adjacent_cells) == 0:
                    continue

                level_up_chance = random.randint(0,self.conf['plants'].getint('seed_chance'))
                if level_up_chance == 0:
                    x, y = random.choice(empty_adjacent_cells)
                    self.place_gamepiece(Plant, x, y)
