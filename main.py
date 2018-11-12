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

slimeList1 = arcade.SpriteList()
slimeList2 = arcade.SpriteList()

def placeSlimes(id, num_one, num_two, sprite_scaling, map):
    # Set a given number of points in the matix to be plants spots
    print("Placing slimes")

    slimeCount = 0
    while slimeCount < (num_one + num_two):
        randX = random.randint(0, map.row_count() / 2 - 1)
        randY = random.randint(0, map.column_count() - 1)
        if map.get_matrix()[randX][randY] == 0:
            slime = arcade.Sprite("images/slime.png", sprite_scaling)
            slime.x = randX
            slime.y = randY
            slimeList1.append(slime)

            slime = arcade.Sprite("images/slime.png", sprite_scaling)
            slime.x = map.row_count() - randX
            slime.y = map.column_count() - randY
            slimeList2.append(slime)
        
            slimeCount +=2

            map.get_matrix()[randX][randY] = id
            map.get_matrix()[map.row_count() - 1 - randX][map.column_count() - 1 - randY] = id

class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, config):
        super().__init__(config['screen'].getint('width'),
                         config['screen'].getint('height'),
                         "SlimeMind")
        # config
        self.width = config['screen'].getint('width')
        self.height = config['screen'].getint('height')
        self.conf = config

        # initial game state
        self.map = Map(config)
        self.plant_list = arcade.SpriteList()
        self.all_sprites_list = arcade.SpriteList()
        self.turn = 0
        self.player_one = PlayerOne()
        self.player_two = PlayerTwo()

        arcade.set_background_color(arcade.color.ALMOND)

    # Evaluate and exicute command
    def movement(self,command,slime,column_count, row_count):
        if command is Commands.UP and slime.y < self.map.column_count():
            slime.y +=1
        elif command is Commands.DOWN and slime.y > 0:
            slime.y -=1
        elif command is Commands.RIGHT and slime.x < self.map.row_count():
            slime.x +=1
        elif command is Commands.LEFT and slime.x >0:
            slime.x -=1
        return slime

    def setup(self):
        """ Initialize game state """
        # place slimes
        placeSlimes(self.conf['slimes']['id'],
                self.conf['slimes'].getint('num_one'),
                self.conf['slimes'].getint('num_two'),
                self.conf['slimes'].getfloat('sprite_scaling'),
                self.map)
        # Create the plants
        for i in range(self.conf['plants'].getint('num_total')//2):
            rand_x = random.randint(1, self.map.row_count() / 2)
            rand_y = random.randint(1, self.map.column_count())
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

    def on_draw(self):
        """
        Render the screen.
        """
        arcade.start_render()
        self.all_sprites_list.draw()

        # Draw slimes    
        for i in range(self.conf['slimes'].getint('num_one')):
            slimeList1[i].center_x = self.map.center_x(slimeList1[i].x)
            slimeList1[i].center_y = self.map.center_x(slimeList1[i].y)
            radius = (self.height//self.map.column_count())//3
            arcade.draw_circle_filled(slimeList1[i].center_x, slimeList1[i].center_y, radius, arcade.color.BLUE)
            slimeList1[i].draw()

        for i in range(self.conf['slimes'].getint('num_two')):
            slimeList2[i].center_x = self.map.center_x(slimeList2[i].x)
            slimeList2[i].center_y = self.map.center_x(slimeList2[i].y)
            radius = (self.height//self.map.column_count())//3
            arcade.draw_circle_filled(slimeList2[i].center_x, slimeList2[i].center_y, radius, arcade.color.RED)
            slimeList2[i].draw()

        # Put the text on the screen.
        output = "turn: {}".format(self.turn)
        arcade.draw_text(output, 10, 20, arcade.color.BLACK, 14)

    def update(self, delta_time):
        """ Movement and game logic """
        # allow all sprites to handle their own update
        self.all_sprites_list.update()

        # handle collisions
        # TODO: include slimes
        for plant in self.plant_list:
            # TODO: I think this should be all_sprites_list once we add in slimes to it
            # level up plant for everything it hits that isn't a plant or on a chance basis?
            hits = arcade.check_for_collision_with_list(plant, slimeList1)
            hits = hits + arcade.check_for_collision_with_list(plant, slimeList2)
            for hit in hits:
                if not isinstance(hit, Plant):
                    plant.level_up()

        UpgradeChance = 0

        # Turn counter
        self.turn += 1
        
        # Call external function for player 1 slimes
        for i in range(self.conf['slimes'].getint('num_one')):
            command = self.player_one.command_slime(self.map, {})
            
            slimeList1[i].x=MyGame.movement(self,command,slimeList1[i],self.map.column_count(),self.map.row_count()).x
            slimeList1[i].y=MyGame.movement(self,command,slimeList1[i],self.map.column_count(),self.map.row_count()).y
            
            # Check for collisions
            collision = 0
            for j in range(len(slimeList1)):
                if slimeList1[i].x == slimeList1[j].x and slimeList1[i].y == slimeList1[j].y and not i == j:
                    collision = 1
            for j in range(len(slimeList2)):
                if slimeList1[i].x == slimeList2[j].x and slimeList1[i].y == slimeList2[j].y:
                    collision = 1

            # If there is a collision revert motion
            if collision:
                if command is Commands.UP :
                    slimeList1[i].y -=1
                if command is Commands.DOWN:
                    slimeList1[i].y +=1
                if command is Commands.RIGHT:
                    slimeList1[i].x -=1
                if command is Commands.LEFT:
                    slimeList1[i].x +=1

        # Call external function for player 2 slimes
        for i in range(self.conf['slimes'].getint('num_two')):
            
            command = self.player_two.command_slime(self.map, {})

            slimeList2[i].x=MyGame.movement(self,command,slimeList2[i],self.map.column_count(),self.map.row_count()).x
            slimeList2[i].y=MyGame.movement(self,command,slimeList2[i],self.map.column_count(),self.map.row_count()).y

            # Check for collisions
            collision = 0
            for j in range(len(slimeList1)):
                if slimeList2[i].x == slimeList1[j].x and slimeList2[i].y == slimeList2[j].y and not i == j:
                    collision = 1
            for j in range(len(slimeList2)):
                if slimeList2[i].x == slimeList1[j].x and slimeList2[i].y == slimeList1[j].y:
                    collision = 1

            # If there is a collision revert motion
            if collision:
                if command is Commands.UP :
                    slimeList2[i].y -=1
                if command is Commands.DOWN:
                    slimeList2[i].y +=1
                if command is Commands.RIGHT:
                    slimeList2[i].x -=1
                if command is Commands.LEFT:
                    slimeList2[i].x +=1

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

