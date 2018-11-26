import arcade
import random
import os
import time
import logging
import csv

from visualizer.plant_sprite import PlantSprite
from visualizer.slime_sprite import SlimeSprite
from visualizer.rock_sprite import RockSprite
from timer.timer import turn_timer

class Visualizer(arcade.Window):
    """ Main application class. """

    def __init__(self, config, initial_state, get_state):
        super().__init__(config['screen'].getint('width'),
                         config['screen'].getint('height'),
                         "SlimeMind")
        # config
        self.conf = config
        self.width = config['screen'].getint('width')
        self.height = config['screen'].getint('height')
        self.step_x = self.width // (config['screen'].getint('columns'))
        self.step_y = self.height // (config['screen'].getint('rows'))

        # initial game state
        self.all_sprites_list = arcade.SpriteList(use_spatial_hash=False)
        self.turn = 0
        self.start = 0
        self.get_state = get_state
        # initialize sprites
        for piece in self.flatten_state(initial_state):
            self.add_sprite(piece)

    def set_sprite_position(self, sprite, x, y):
        center_x = (x + 1/2) * self.step_x
        center_y = (y + 1/2) * self.step_y
        if self.turn == 0 or sprite.center_x != center_x or sprite.center_y != center_y:
            sprite.set_position(center_x, center_y)

    def flatten_state(self, state):
        flat = []
        for x in range(len(state)):
            for y in range(len(state[x])):
                piece = state[x][y]
                if piece is not None:
                    flat.append(piece)
        return flat

    def hashify_state(self, state):
        flat = self.flatten_state(state)
        state_dict = {}
        for piece in flat:
            state_dict[piece['id']] = piece
        return state_dict

    def add_sprite(self, piece):
        if piece['type'] == 'PLANT':
            sprite = PlantSprite(self.conf['Plant'], piece['id'])
            self.set_sprite_position(sprite, piece['x'], piece['y'])
        elif piece['type'] == 'SLIME':
            sprite = SlimeSprite(self.conf['Slime'], piece['id'])
            self.set_sprite_position(sprite, piece['x'], piece['y'])
        elif piece['type'] == 'ROCK':
            sprite = RockSprite(self.conf['Rock'], piece['id'])
            self.set_sprite_position(sprite, piece['x'], piece['y'])
        else:
            raise Exception("Unrecognized piece type")
        self.all_sprites_list.append(sprite)

    def draw_grid(self):
        # TODO: fix this
        # Draw a grid based on map.py center_x and center_y functions
        for row in range(self.map.rows):
            for column in range(self.map.columns):
                # Figure out what color to draw the box
                color = arcade.color.ALMOND

                # Do the math to figure out where the box is
                x_box = (self.map.width/self.map.columns) * (column) + (self.map.width/self.map.columns)/2
                y_box = (self.map.height/self.map.rows)* (row) + (self.map.height/self.map.rows)/2

                # Draw the box
                arcade.draw_rectangle_filled(x_box, y_box, self.map.width/self.map.columns-2, self.map.height/self.map.rows-2, color)

    def on_draw(self):
        """Render the screen."""
        arcade.start_render()
        arcade.set_background_color(arcade.color.AMAZON)
        #self.draw_grid()
        turn_timer(self.all_sprites_list.draw, self.turn)()

        # Put the text on the screen.
        elapsed = time.perf_counter() - self.start
        self.start = time.perf_counter()
        output = f"turn: {self.turn} seconds since last turn: {elapsed}"
        print(f"timer,{self.turn},full_turn,{elapsed}")
        arcade.draw_text(output, 10, 20, arcade.color.BLACK, 14)

        # Delay to slow game down        
        time.sleep(self.conf['misc'].getfloat('sleep'))

    def handle_sprite(self, sprite, state_dict):
        """ Removes, moves, and updates textures of a sprite based on state"""
        # rocks never change
        if type(sprite) is RockSprite:
            return

        # check for death
        if sprite.id not in state_dict:
            sprite.kill()
            return

        piece = state_dict[sprite.id]
        # update textures based on level
        sprite.update_texture(piece)

        # movement
        if type(sprite) is SlimeSprite:
            self.set_sprite_position(sprite, piece['x'], piece['y'])

    def add_sprites(self, state_dict, ids):
        for piece in state_dict.values():
            if piece['id'] not in ids:
                self.add_sprite(piece)

    def update(self, delta_time):
        """ Movement and game logic """
        state = turn_timer(self.get_state, self.turn)()
        # stop visualizing when there's no more state to render
        if state is False:
            arcade.window_commands.close_window()
            return

        # Turn counter
        self.turn += 1

        state_dict = turn_timer(self.hashify_state, self.turn)(state)

        ids = []
        for sprite in self.all_sprites_list:
            # track ids of existing sprites so we can add mising ones
            ids.append(sprite.id)
            # kill or update sprites
            turn_timer(self.handle_sprite, self.turn)(sprite, state_dict)

        # add new sprites
        turn_timer(self.add_sprites, self.turn)(state_dict, ids)
