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
import csv

# Import classes
from models.plant import Plant
from models.slime import Slime
from models.rock import Rock
from models.map import Map
from models.commands import Commands
from models.sprite_man import Sprite_man

# Import player's AIs, TODO make the program pick the player files to import from but hand enetering for now is fine.
# player_codes = os.listdir(os.path.dirname(os.path.realpath(__file__))+'\PlayerCode')
# print(player_codes)
# code1 = None
# code2 = None

# code1 = player_codes[random.randint(0,len(player_codes)-2)]
# code1 = 'PlayerCode.' + code1[0:len(code1)-3]
# print( 'Code1 is', code1)
# while not code2:
#     option = player_codes[random.randint(0,len(player_codes)-2)]
#     if option != code1:
#         code2 = 'PlayerCode.' + option[0:len(option)-3]
# print( 'Code2 is', code2)

from PlayerCode.player_one import Player as PlayerOne
from PlayerCode.player_three import Player as PlayerTwo

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

    def __init__(self, config, player_one, player_two):
        super().__init__(config['screen'].getint('width'),
                         config['screen'].getint('height'),
                         "SlimeMind")
        # config
        self.width = config['screen'].getint('width')
        self.height = config['screen'].getint('height')
        self.num_slimes = config['slimes'].getint('num_total')
        self.max_turns = config['screen'].getint('max_turns')
        self.conf = config

        # initial game state
        self.map = Map(config)
        self.all_sprites_list = arcade.SpriteList()
        self.sprite_man = Sprite_man(self.map, self.conf, self.all_sprites_list)
        self.turn = 0
        self.player_one = player_one
        self.player_two = player_two

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
    def drop_rocks(self):
        rocks = 0
        while rocks < self.conf['rocks'].getint('num_total'):
            rand_x = random.randint(0, self.map.column_count() / 2 -1)
            rand_y = random.randint(0, self.map.row_count()-1 )
            if self.map.is_cell_empty(rand_x, rand_y):
                # left half
                self.sprite_man.drop_rock(rand_x, rand_y)
                # mirrored across x and y axis for right half
                self.sprite_man.drop_rock((self.map.column_count() - 1) - rand_x, (self.map.row_count() - 1) - rand_y)
                rocks += 2

    @trace
    def bite_thing(self, command, x, y, attack):
        # Slime tries to bite a target, then if succesful this method awards 1 xp
        (x, y) = command.update_coord(x, y)
        target = self.map.matrix[x][y]

        # Make sure target is in map range
        if not self.map.valid_coord(x, y) or type(target) is Rock:
            return 0
        elif target is not None:
            target.current_hp -= attack
            return 1 if type(target) is Slime else 2

    @trace
    def split(self, slime):
        """ split slime into random empty adjacent cell """
        empty_adjacent_cells = self.map.adjacent_empty_cells(slime.x, slime.y)

        # can't split if there are no available cells
        if len(empty_adjacent_cells) == 0:
            return
        
        # can't split if the slime is not high enough level
        if slime.level >= self.conf['slimes'].getint('min_split_level'):
            x, y = random.choice(empty_adjacent_cells)
            slime.split()

            if slime.player == 1:
                self.place_slime(x, y, 1)
            else:
                self.place_slime(x, y, 2)
    
    @trace
    def end_game(self):
        """ Print winner, generate report, ... """
        arcade.window_commands.close_window()
        results = {}
        results['winner'] = 'tie'
        results['final turn'] = self.turn
        results['player one score'] = 0
        results['player two score'] = 0
        results['player one max slime level'] = 0
        results['player two max slime level'] = 0
        results['player one slime count'] = 0
        results['player two slime count'] = 0

        for slime in self.all_sprites_list:
            if type(slime) is Slime and slime.player == 1:
                results['player one slime count'] += 1
                results['player one score'] += int(slime.level**(3/2))
                if results['player one max slime level'] < slime.level:
                    results['player one max slime level'] = slime.level

            if type(slime) is Slime and slime.player == 2:
                results['player two slime count'] += 1
                results['player two score'] += int(slime.level**(3/2))
                if results['player two max slime level'] < slime.level:
                    results['player two max slime level'] = slime.level

        if results['player one score'] > results['player two score']:
            results['winner'] = self.player_one.name
        elif results['player one score'] < results['player two score']:
            results['winner'] = self.player_two.name

        print('GAME OVER')
        for k, v in results.items():
            print(k, v)
        with open('results.csv', 'a', newline = '') as f:
            writer = csv.DictWriter(f, fieldnames = results.keys())
            writer.writerow(results)

    @trace
    def execute_round(self, slime, player):
        command = player.command_slime(self.map, slime, self.turn)
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

        if command is Commands.SPLIT:
            self.split(slime)

        if command is Commands.MERGE:
            slime.ready_to_merge = True

        self.sprite_man.check_for_dead()
        self.sprite_man.check_for_merge()


    @trace
    def setup(self):
        """ Initialize game state """
        self.place_slimes()
        self.plant_plants()
        self.drop_rocks()

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
    def slime_sprite_update(self):
        """Update the slimes sprites based on player and level."""
        scale = self.conf['slimes'].getfloat('sprite_scaling')
        min_split_level = self.conf['slimes'].getint('min_split_level') * 2

        for slime in self.all_sprites_list:
            if type(slime) is Slime:
                if slime.player == 1:
                    if slime.level < min_split_level:
                        filename = self.conf['slimes'].get('filename1')
                    else:
                        filename = self.conf['slimes'].get('filename3')
                else:
                    if slime.level < min_split_level:
                        filename = self.conf['slimes'].get('filename2')
                    else:
                        filename = self.conf['slimes'].get('filename4')
                slime.texture=arcade.draw_commands.load_texture(filename, scale=scale)

    @trace
    def on_draw(self):
        """Render the screen."""
        if self.conf['misc'].get('render') == 'True':
            arcade.start_render()
            arcade.set_background_color(arcade.color.AMAZON)
            #self.draw_grid()
            self.slime_sprite_update()
            self.all_sprites_list.draw()

            # Put the text on the screen.
            output = "turn: {}".format(self.turn)
            arcade.draw_text(output, 10, 20, arcade.color.BLACK, 14)

            # Delay to slow game down        
            time.sleep(self.conf['misc'].getfloat('sleep'))

    @trace
    def update(self, delta_time):
        """ Movement and game logic """
        # Turn counter
        self.turn += 1
        
        # allow all sprites to handle their own update
        self.all_sprites_list.update()

        # check to see if the plants spread seeds
        self.sprite_man.spread_seeds()

        player1_slime_count = 0
        player2_slime_count = 0

        # Call external function for player 1 slimes
        for slime in self.all_sprites_list:
            if type(slime) is Slime and slime.player == 1:
                self.execute_round(slime, self.player_one)
                player1_slime_count += 1

                # Call external function for player 2 slimes
            if type(slime) is Slime and slime.player == 2:
                self.execute_round(slime, self.player_two)
                player2_slime_count += 1

        # Check for end of game conditions
        if self.turn > self.max_turns or player2_slime_count == 0 or player1_slime_count == 0:
            time.sleep(self.conf['misc'].getfloat('sleep')*50)
            self.end_game()

def main():
    # config
    config = configparser.ConfigParser()
    config.read('resources/config.ini')

    # logging
    logger = logging.getLogger()
    logger.setLevel(config['logging']['level'])
    handler = logging.StreamHandler()
    logger.addHandler(handler)

    # players
    player_one = PlayerOne(1)
    player_two = PlayerTwo(2)

    # run the actual game
    window = MyGame(config, player_one, player_two)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()

