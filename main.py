"""
This program will attempt to set the plants to grow.
"""

# Import libraries
import arcade
import random
import os
import time
import configparser

# Import classes
from models.plant import Plant
from models.slime import Slime
from models.map import Map
from models.commands import Commands

# Import player's AIs, it would be great if we could make the program pick the player files to import from but hand enetering for now is fine.
from player_one import Player as PlayerOne
from player_two import Player as PlayerTwo

x = 0
y = 0

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
        self.turn = 0
        self.player_one = PlayerOne()
        self.player_two = PlayerTwo()

        arcade.set_background_color(arcade.color.BLACK)

    def place_slimes(self):
        print("Placing slimes")

        slimes = 0
        while slimes < self.num_slimes:
            randX = random.randint(1, self.map.row_count() / 2 - 1)
            randY = random.randint(1, self.map.column_count() - 1)
            if self.map.get_matrix()[randX][randY] == 0:
                # player one
                slime = Slime('fake_id', self.conf, self.map)
                slime.set_coord(randX, randY)
                self.slimes_one.append(slime)
                self.all_sprites_list.append(slime)

                # player two
                slime = Slime('fake_id', self.conf, self.map)
                slime.set_coord(self.map.row_count() - randX, self.map.column_count() - randY)
                self.slimes_two.append(slime)
                self.all_sprites_list.append(slime)

                slimes += 2

    def place_plants(self):
        print("Placing plants")
        # Create the plants
        for i in range(self.conf['plants'].getint('num_total')//2):
            rand_x = random.randint(1, self.map.row_count() / 2 - 1)
            rand_y = random.randint(1, self.map.column_count() - 1)
            # left half
            plant = Plant(i, self.conf, self.map)
            plant.set_coord(rand_x, rand_y)
            self.all_sprites_list.append(plant)
            self.plant_list.append(plant)

            # mirrored across x and y axis for right half
            plant = Plant(i, self.conf, self.map)
            plant.set_coord(self.map.row_count() - rand_x,self.map.column_count() - rand_y)
            self.all_sprites_list.append(plant)
            self.plant_list.append(plant)



    def move(self, command, x, y):
        if command is Commands.UP and y < self.map.column_count() - 1:
            y += 1
        elif command is Commands.DOWN and y > 0:
            y -= 1
        elif command is Commands.RIGHT and x < self.map.row_count() - 1:
            x += 1
        elif command is Commands.LEFT and x > 0:
            x -= 1
        return (x, y)

    def execute_round(self, slime, player):
        command = player.command_slime(self.map, slime)

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

    def setup(self):
        """ Initialize game state """
        self.place_slimes()
        self.place_plants()
        

    def on_draw(self):
        """
        Render the screen.
        """
        arcade.start_render()
        self.all_sprites_list.draw()

        # Draw a grid based on map.py center_x and center_y functions
        for row in range(2):
            for column in range(2):
                # Figure out what color to draw the box
                color = arcade.color.ALMOND

                # Do the math to figure out where the box is
                x_box = (1200/30)/2 * (column+1) 
                y_box = (600/15)/2 * (row+1) 

                # Draw the box
                arcade.draw_rectangle_filled(x_box, y_box, self.map.step_x-5, self.map.step_y-5, color)


                #arcade.draw_rectangle_filled((600/15)/2, (1200/30)/2, self.map.step_x-5, self.map.step_y-5, color)

        # Put the text on the screen.
        output = "turn: {}".format(self.turn)
        arcade.draw_text(output, 10, 20, arcade.color.BLACK, 14)

    def update(self, delta_time):
        """ Movement and game logic """
        # allow all sprites to handle their own update
        self.all_sprites_list.update()

        # Add sprite manager, and map manager

        # Turn counter
        self.turn += 1
        
        # Call external function for player 1 slimes
        for slime in self.slimes_one:
            self.execute_round(slime, self.player_one)

            # Add sprite manager, and map manager

        # Call external function for player 2 slimes
        for slime in self.slimes_two:
            self.execute_round(slime, self.player_two)

            # Add sprite manager, and map manager

        # Delay to slow game down        
        time.sleep(0.01)

def main():
    config = configparser.ConfigParser()
    config.read('resources/config.ini')
    window = MyGame(config)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()

