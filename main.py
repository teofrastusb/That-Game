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
        self.all_sprites_list = arcade.SpriteList()
        self.sprite_man = Sprite_man(self.map, self.conf, self.all_sprites_list)
        self.turn = 0
        self.player_one = PlayerOne(1)
        self.player_two = PlayerTwo(2)

        arcade.set_background_color(arcade.color.BLACK)

    @trace 
    def place_slime(self, x, y, player):
        slime = Slime(uuid.uuid4(), self.conf, self.map, player)
        slime.set_coord(x, y)
        self.all_sprites_list.append(slime)

    @trace
    def place_slimes(self):
        slimes = 0
        while slimes < self.num_slimes:
            randX = random.randint(1, self.map.column_count() / 2 -1)
            randY = random.randint(1, self.map.row_count() -1)
            if self.map.is_cell_empty(randX, randY):
                # player one
                self.place_slime(randX, randY, 1)
                # player two
                self.place_slime(self.map.column_count() - randX, self.map.row_count() - randY, 2)
                slimes += 2

    @trace
    def plant_plants(self):
        plants = 0
        while plants < self.conf['plants'].getint('num_total'):
            rand_x = random.randint(0, self.map.column_count() / 2 -1)
            rand_y = random.randint(0, self.map.row_count()-1 )
            if self.map.is_cell_empty(rand_x, rand_y):
                # left half
                self.sprite_man.place_plant(rand_x, rand_y)
                # mirrored across x and y axis for right half
                self.sprite_man.place_plant((self.map.column_count() - 1) - rand_x, (self.map.row_count() - 1) - rand_y)
                plants += 2

    @trace
    def bite_thing(self, command, x, y, attack):
        # Slime tries to bite a target, then if succesful this method awards 1 xp
        (x, y) = command.update_coord(x, y)

        #print('slime is tring to ', command)

        # Make sure target is in map range
        if not self.map.valid_coord(x, y):
            return 0

        target = self.map.matrix[x][y]
        # Check if target is a slime
        if target != 0 and hasattr(target, 'player'):
            target.current_hp -= attack
            return 1

        elif target != 0:
            target.current_hp -= attack
            return 2

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
    def end_game(self):
    # Print winner, generate report, ...
        pass

    @trace
    def execute_round(self, slime, player):
        command = player.command_slime(self.map, slime)
        # allow player to take no action
        if command is None:
            return

        # Check for move commands
        if command.is_move():
            # Attempt to move the slime if the target cell is empty
            (x, y) = command.update_coord(slime.x, slime.y)
            if self.map.valid_coord(x, y) and self.map.is_cell_empty(x, y):
                slime.set_coord(x, y)

        # Check for bite commands
        if (command.is_bite()):
            # Attempt to bite things
            hit = self.bite_thing(command, slime.x, slime.y, slime.attack)
            #print('if 1 then hit', hit)
            if hit:
                slime.xp += 1
                hit -= 1
                if hit:
                    slime.current_hp += slime.hp_increment//slime.hp_increment

        if (command is Commands.SPLIT):
            self.split(slime)

        # TODO Check for merge command

        self.sprite_man.check_for_dead()

    @trace
    def setup(self):
        """ Initialize game state """
        self.place_slimes()
        self.plant_plants()

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
        for slime in self.all_sprites_list:
            if type(slime) is Slime and slime.player == 1:
                self.execute_round(slime, self.player_one)

        # Call external function for player 2 slimes
        for slime in self.all_sprites_list:
            if type(slime) is Slime and slime.player == 2:
                self.execute_round(slime, self.player_two)

        # Delay to slow game down        
        time.sleep(self.conf['misc'].getfloat('sleep'))

        # Check for end of game conditions, TODO add one team of slimes is empty
        # if self.turn > self.conf['screen'].getint('max_turn'):
        #     print('In endgame')
        #     #self.end_game()
        #     arcade.window_commands.close_window()

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

