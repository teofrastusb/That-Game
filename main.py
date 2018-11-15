"""
This program will attempt to set the plants to grow.
"""

# Import libraries
import arcade
import random
import os
import time
import configparser
import logging
import uuid

# Import classes
from models.plant import Plant
from models.slime import Slime
from models.map import Map
from models.commands import Commands
from models.sprite_man import Sprite_man

# Import player's AIs, it would be great if we could make the program pick the player files to import from but hand enetering for now is fine.
from player_one import Player as PlayerOne
from player_two import Player as PlayerTwo

# log debug message for decorated methods
def trace(function):
    def wrapper(*args, **kwargs):
        logging.getLogger().debug("method: %s args: %s ", function.__name__, str(args))
        ret = function(*args, **kwargs)
        logging.getLogger().debug("exiting: %s", function.__name__)
        return ret
    return wrapper

class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, config):
        super().__init__(config['screen'].getint('width'),
                         config['screen'].getint('height'),
                         "SlimeMind")
        # config
        self.width = config['screen'].getint('width')
        self.height = config['screen'].getint('height')
        self.num_slimes = config['slimes'].getint('num_total')
        self.conf = config

        # initial game state
        self.map = Map(config)
        self.plant_list = arcade.SpriteList()
        self.slimes_one = arcade.SpriteList()
        self.slimes_two = arcade.SpriteList()
        self.all_sprites_list = arcade.SpriteList()
        self.sprite_man = Sprite_man(self.map, self.conf, self.plant_list, self.slimes_one, self.slimes_two, self.all_sprites_list)
        self.turn = 0
        self.player_one = PlayerOne()
        self.player_two = PlayerTwo()

        arcade.set_background_color(arcade.color.BLACK)

    @trace 
    def place_slime(self, x, y, player):
        slime = Slime(uuid.uuid4(), self.conf, self.map, player)
        slime.set_coord(x, y)
        if player == 1:
            self.slimes_one.append(slime)
        else:
            self.slimes_two.append(slime)
        self.all_sprites_list.append(slime)

    @trace
    def place_slimes(self):
        slimes = 0
        while slimes < self.num_slimes:
            randX = random.randint(1, self.map.column_count() / 2 -1)
            randY = random.randint(1, self.map.row_count() -1)
            if self.map.cell_empty(randX, randY):
                # player one
                self.place_slime(randX, randY, 1)
                # player two
                self.place_slime(self.map.column_count() - randX, self.map.row_count() - randY, 2)
                slimes += 2

    @trace
    def place_plants(self):
        # Create the plants
        for i in range(self.conf['plants'].getint('num_total')//2):
            rand_x = random.randint(0, self.map.column_count() / 2 -1)
            rand_y = random.randint(0, self.map.row_count()-1 )
            # left half
            self.sprite_man.place_plant(rand_x, rand_y)
            # mirrored across x and y axis for right half
            self.sprite_man.place_plant((self.map.column_count() - 1) - rand_x, (self.map.row_count() - 1) - rand_y)

    @trace
    def move(self, command, x, y):
        (x_prime, y_prime) = command.update_coord(x, y)
        if self.map.valid_coord(x_prime, y_prime):
            return (x_prime, y_prime)
        return (x, y)

    @trace
    def bite_thing(self, command, x, y, attack):
        # Slime tries to bite a target, then if succesful this method awards 1 xp
        (x, y) = command.update_coord(x, y)

        # Make sure target is in map range
        if not self.map.valid_coord(x, y):
            return 0

        target = self.map.matrix[x][y]
        # Check if target is a plant or slime
        if target != 0:
            target.current_hp -= attack
            return 1

    @trace
    def split(self, slime):
        """ split slime into random empty adjacent cell """
        empty_adjacent_cells = self.map.adjacent_empty_cells(slime.x, slime.y)

        # can't split if there are no available cells
        if len(empty_adjacent_cells) == 0:
            return

        x, y = random.choice(empty_adjacent_cells)
        slime.split()

        if slime.player == 1:
            self.place_slime(x, y, 1)
        else:
            self.place_slime(x, y, 2)

    @trace
    def execute_round(self, slime, player):
        command = player.command_slime(self.map, slime)
        # allow player to take no action
        if command is None:
            return

        # Check for move commands
        if command.is_move():
            # Attempt to move the slime
            original_x, original_y = slime.x, slime.y
            x, y = self.move(command, slime.x, slime.y)
            slime.set_coord(x, y)
            self.map.clear_cell(original_x, original_y)
            
            # If there is a collision revert move
            hits = arcade.check_for_collision_with_list(slime, self.all_sprites_list)
            if len(hits) > 0:
                slime.set_coord(original_x, original_y)
                self.map.clear_cell(x, y)

        # Check for bite commands
        if (command.is_bite()):
            # Attempt to bite things
            hit = self.bite_thing(command, slime.x, slime.y, slime.attack)
            if hit:
                slime.xp += 1

        # TODO Check for split command
        if (command is Commands.SPLIT):
            self.split(slime)

        # TODO Check for merge command

    @trace
    def setup(self):
        """ Initialize game state """
        self.place_slimes()
        self.place_plants()

    @trace
    def draw_grid(self):
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

    @trace
    def on_draw(self):
        """
        Render the screen.
        """
        arcade.start_render()
        self.draw_grid()
        self.all_sprites_list.draw()

        # Put the text on the screen.
        output = "turn: {}".format(self.turn)
        arcade.draw_text(output, 10, 20, arcade.color.BLACK, 14)

    @trace
    def update(self, delta_time):
        """ Movement and game logic """
        # Turn counter
        self.turn += 1
        
        # allow all sprites to handle their own update
        self.all_sprites_list.update()

        self.sprite_man.spread_seeds()

        # Call external function for player 1 slimes
        for slime in self.slimes_one:
            self.execute_round(slime, self.player_one)

            # Sprite manager check for dead
            self.sprite_man.check_for_dead()

        # Call external function for player 2 slimes
        for slime in self.slimes_two:
            self.execute_round(slime, self.player_two)

            # Sprite manager check for dead
            self.sprite_man.check_for_dead()

        # Delay to slow game down        
        time.sleep(self.conf['misc'].getfloat('sleep'))

def main():
    config = configparser.ConfigParser()
    config.read('resources/config.ini')

    logger = logging.getLogger()
    logger.setLevel(config['logging']['level'])
    handler = logging.StreamHandler()
    logger.addHandler(handler)

    window = MyGame(config)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()

