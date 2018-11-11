#!/usr/bin/env python

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
from plant import Plant
from slime import Slime

# Import control functions
from tet import Tet
class Player1(Tet): 
    def printPlayer():
        print("Player1")

class Player2(Tet):
    def printPlayer():
        print("Player2")

x = 0
y = 0
turn = 0

mapMatrix = []

plantlist = arcade.SpriteList()
slimelist1 = arcade.SpriteList()
slimelist2 = arcade.SpriteList()

"""
plantlist = [Plant() for i in range(numPlants)]
slimelist = [Slime() for i in range(numSlimes1)]
"""

def makeMatrix(width, height):
    # Setup an empty matrix of the correct size
    print("Making matrix")

    for i in range(width):
        mapMatrix.append([0]*height)

def plantPlants(id, numPlants, num_x, num_y, sprite_scaling):
    # Set a given number of points in the matix to be plants spots
    print("Planting plants")

    plantCount = 0
    while plantCount < numPlants:
        randX = random.randint(0,num_x/2-1)
        randY = random.randint(0,num_y-1)
    
        #print(randX,randY)
    
        if mapMatrix[randX][randY] == 0:

            plant = arcade.Sprite("plant.jpg", sprite_scaling)
        
            plant.x = randX
            plant.y = randY
            plant.level = 1
            plant.health = 10

            plantlist.append(plant)


            plant = arcade.Sprite("plant.jpg", sprite_scaling)
        
            plant.x = num_x-randX
            plant.y = num_y-randY
            plant.level = 1
            plant.health = 10

            plantlist.append(plant)
        
            plantCount = plantCount+2

            mapMatrix[randX][randY] = id
            mapMatrix[num_x-1-randX][num_y-1-randY] = id

def placeSlimes(id, num_one, num_two, sprite_scaling, num_x, num_y):
    # Set a given number of points in the matix to be plants spots
    print("Placing slimes")

    slimeCount = 0
    while slimeCount < (num_one + num_two):
        randX = random.randint(0,num_x/2-1)
        randY = random.randint(0,num_y-1)
    
        #print(randX,randY)
    
        if mapMatrix[randX][randY] == 0:

            slime = arcade.Sprite("slime.jpg", sprite_scaling)
            slime.x = randX
            slime.y = randY
            slimelist1.append(slime)

            slime = arcade.Sprite("slime.jpg", sprite_scaling)
            slime.x = num_x-randX
            slime.y = num_y-randY
            slimelist2.append(slime)
        
            slimeCount +=2

            mapMatrix[randX][randY] = id
            mapMatrix[num_x-1-randX][num_y-1-randY] = id

class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, config):
        super().__init__(config['screen'].getint('width'),
                         config['screen'].getint('height'),
                         "SlimeMind")
        self.width = config['screen'].getint('width')
        self.height = config['screen'].getint('height')
        self.num_x = config['screen'].getint('num_x')
        self.num_y = config['screen'].getint('num_y')
        self.conf = config

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        arcade.set_background_color(arcade.color.ALMOND)

        StepX = self.width // (self.num_x + 2)
        StepY = self.height // (self.num_y + 2)

        # Draw plants
        for i in range(self.conf['plants'].getint('num_total')):
            plantlist[i].center_x = (plantlist[i].x+1)*StepX
            plantlist[i].center_y = (plantlist[i].y+1)*StepY
            
            #print(plantlist[i].center_X,plantlist[i].center_Y)
            plantlist[i].draw()

            radius = (self.height//self.num_y)//4 * plantlist[i].level/10
            arcade.draw_circle_filled(plantlist[i].center_x, plantlist[i].center_y, radius, arcade.color.GREEN)

        # Draw slimes    
        for i in range(self.conf['slimes'].getint('num_one')):
            slimelist1[i].center_x = (slimelist1[i].x+1)*StepX
            slimelist1[i].center_y = (slimelist1[i].y+1)*StepY
            radius = (self.height//self.num_y)//3
            arcade.draw_circle_filled(slimelist1[i].center_x, slimelist1[i].center_y, radius, arcade.color.BLUE)
            slimelist1[i].draw()

        for i in range(self.conf['slimes'].getint('num_two')):
            slimelist2[i].center_x = (slimelist2[i].x+1)*StepX
            slimelist2[i].center_y = (slimelist2[i].y+1)*StepY
            radius = (self.height//self.num_y)//3
            arcade.draw_circle_filled(slimelist2[i].center_x, slimelist2[i].center_y, radius, arcade.color.RED)
            slimelist2[i].draw()

        # Put the text on the screen.
        output = "turn: {}".format(turn)
        arcade.draw_text(output, 10, 20, arcade.color.BLACK, 14)

    def update(self, delta_time):
        """ Movement and game logic """
        UpgradeChance = 0

        # Turn counter
        global turn
        turn += 1
        
        # Grow the plants
        for i in range(self.conf['plants'].getint('num_total')):
            UpgradeChance = random.randint(0,20)//1
            if UpgradeChance > plantlist[i].level:
                UpgradeChance = random.randint(0,20)//1
                if UpgradeChance > plantlist[i].level:
                    plantlist[i].level += 1
        
        # Call external function for slimes
        for i in range(self.conf['slimes'].getint('num_one')):
            command = Player1.playerCommand(1)
            
            # Evaluate and exicute command
            if command == "up" and slimelist1[i].y < self.num_y:
                slimelist1[i].y +=1
            if command == "down" and slimelist1[i].y > 0:
                slimelist1[i].y -=1
            if command == "right" and slimelist1[i].x < self.num_x:
                slimelist1[i].x +=1
            if command == "left" and slimelist1[i].x >0:
                slimelist1[i].x -=1

        # Call external function for slimes
        for i in range(self.conf['slimes'].getint('num_two')):
            command = Player2.playerCommand(1)

            # Evaluate and exicute command
            if command == "up" and slimelist2[i].y < self.num_y:
                slimelist2[i].y +=1
            if command == "down" and slimelist2[i].y > 0:
                slimelist2[i].y -=1
            if command == "right" and slimelist2[i].x < self.num_x:
                slimelist2[i].x +=1
            if command == "left" and slimelist2[i].x >0:
                slimelist2[i].x -=1

        # Delay to slow game down        
        time.sleep(0.1)

def main():
    config = configparser.ConfigParser()
    config.read('resources/config.ini')

    makeMatrix(config['screen'].getint('num_x'), config['screen'].getint('num_x'))
    plantPlants(config['plants'].getint('id'),
                config['plants'].getint('num_total'),
                config['screen'].getint('num_x'),
                config['screen'].getint('num_y'),
                config['plants'].getfloat('sprite_scaling'))
    placeSlimes(config['slimes']['id'],
                config['slimes'].getint('num_one'),
                config['slimes'].getint('num_two'),
                config['slimes'].getfloat('sprite_scaling'),
                config['screen'].getint('num_x'),
                config['screen'].getint('num_y'))
    MyGame(config)
    arcade.run()

if __name__ == "__main__":
    main()

