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
from models.sprite_man import Sprite_man

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
        self.sprite_man = Sprite_man(self.plant_list,self.slimes_one,self.slimes_two)
        self.all_sprites_list = arcade.SpriteList()
        self.turn = 0
        self.player_one = PlayerOne()
        self.player_two = PlayerTwo()

        arcade.set_background_color(arcade.color.BLACK)

    def place_slimes(self):
        print("Placing slimes")

        slimes = 0
        while slimes < self.num_slimes:
            randX = random.randint(1, self.map.column_count() / 2 -1)
            randY = random.randint(1, self.map.row_count() -1)
            if self.map.get_matrix()[randX][randY] == 0:
                # player one
                slime = Slime('fake_id', self.conf, self.map)
                slime.set_coord(randX, randY)
                self.player = 1
                self.slimes_one.append(slime)
                self.all_sprites_list.append(slime)

                # player two
                slime = Slime('fake_id', self.conf, self.map)
                slime.set_coord(self.map.column_count() - randX, self.map.row_count() - randY)
                self.player = 2
                self.slimes_two.append(slime)
                self.all_sprites_list.append(slime)

                slimes += 2

    def place_plants(self):
        print("Placing plants")
        # Create the plants
        for i in range(self.conf['plants'].getint('num_total')//2):
            rand_x = random.randint(0, self.map.column_count() / 2 -1)
            rand_y = random.randint(0, self.map.row_count()-1 )
            # left half
            plant = Plant(i, self.conf, self.map)
            plant.set_coord(rand_x, rand_y)
            self.all_sprites_list.append(plant)
            self.plant_list.append(plant)

            # mirrored across x and y axis for right half
            plant = Plant(i, self.conf, self.map)
            print((self.map.column_count()-1) - rand_x,(self.map.row_count()-1) - rand_y)
            plant.set_coord((self.map.column_count()-1) - rand_x,(self.map.row_count()-1) - rand_y)
            self.all_sprites_list.append(plant)
            self.plant_list.append(plant)



    def move(self, command, x, y):
        if command is Commands.UP and y < self.map.row_count() - 1:
            y += 1
        elif command is Commands.DOWN and y > 0:
            y -= 1
        elif command is Commands.RIGHT and x < self.map.column_count() - 1:
            x += 1
        elif command is Commands.LEFT and x > 0:
            x -= 1
        return (x, y)

    def bite_thing(self, command, x, y,player,attack):
        # Check for bite commands
        if command is Commands.BITEUP:
            # Attempt to bite things above the slime location
            self.damage_thing(x,y+1,player,attack)
        elif command is Commands.BITEDOWN:
            # Attempt to bite things below the slime location
            self.damage_thing(x,y-1,player,attack)
        elif command is Commands.BITELEFT:
            # Attempt to bite things to the left of the slime location
            self.damage_thing(x-1,y,player,attack)
        elif command is Commands.BITERIGHT:
            # Attempt to bite things to the right of the slime location
            self.damage_thing(x+1,y,player,attack)

    def damage_thing(self,x,y,player,attack):
        # Make sure target is in map range
        if x is -1 or x is self.map.column_count() or y is -1 or y is self.map.row_count():
            return

        target = self.map.matrix[x][y]
        # Check if target is a plant or slime
        print("damage_thing current target",target)
        if target != 0:
            if not hasattr(target, 'player') or target.player == player:
                print("damage_thing 2")
                target.current_hp -= attack
                print("target health set to ",target.current_hp)

    def execute_round(self, slime, player):
        command = player.command_slime(self.map, slime)
        #print('Slime for player',slime.player,' has command',command)

        # Check for move commands
        if command is Commands.UP or command is Commands.DOWN or command is Commands.LEFT or command is Commands.RIGHT:
            # print('move loop')
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
        if (command == Commands.BITE or command is Commands.BITEUP or command is Commands.BITEDOWN or 
            command is Commands.BITELEFT or command is Commands.BITERIGHT):
            #print("bite_thing")
            # Attempt to bite things
            self.bite_thing(command, slime.x, slime.y, slime.player, slime.attack)

        # TODO Check for split command

        # TODO Check for merge command

    def setup(self):
        """ Initialize game state """
        self.place_slimes()
        self.place_plants()
        

    def on_draw(self):
        """
        Render the screen.
        """
        arcade.start_render()

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

        self.all_sprites_list.draw()


        # Put the text on the screen.
        output = "turn: {}".format(self.turn)
        arcade.draw_text(output, 10, 20, arcade.color.BLACK, 14)

    def update(self, delta_time):
        """ Movement and game logic """
        # Turn counter
        self.turn += 1
        
        # allow all sprites to handle their own update
        self.all_sprites_list.update()

        # Add sprite manager
        self.sprite_man.check_for_dead(self.map)

        
        # Call external function for player 1 slimes
        for slime in self.slimes_one:
            self.execute_round(slime, self.player_one)

            # Add sprite manager
            self.sprite_man.check_for_dead(self.map)

        # Call external function for player 2 slimes
        for slime in self.slimes_two:
            self.execute_round(slime, self.player_two)

            # Add sprite manager
            self.sprite_man.check_for_dead(self.map)

        # Delay to slow game down        
        time.sleep(0.1)

def main():
    config = configparser.ConfigParser()
    config.read('resources/config.ini')
    window = MyGame(config)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()

