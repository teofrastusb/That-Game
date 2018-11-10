#!/usr/bin/env python

"""
This program will attempt to set the plants to grow.
"""

# Import libraries
import arcade
import random
import os
import time

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

# Manually set constants

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600

SPRITE_SCALING_PLANT = 0.4
SPRITE_SCALING_SLIME = 0.2

numSpacesX = 30
numSpacesY = 15

plantID = 1
slimeID = 2

#Total number of plants
numPlants = 20

#Number of slimes per side
numSlimes1 = 1
numSlimes2 = 1


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

def makeMatrix():
    # Setup an empty matrix of the correct size
    print("Making matrix")

    for i in range(numSpacesX):
        mapMatrix.append([0]*numSpacesY)

def plantPlants():
    # Set a given number of points in the matix to be plants spots
    print("Planting plants")

    plantCount = 0
    while plantCount < numPlants:
        randX = random.randint(0,numSpacesX/2-1)
        randY = random.randint(0,numSpacesY-1)
    
        #print(randX,randY)
    
        if mapMatrix[randX][randY] == 0:

            plant = arcade.Sprite("plant.jpg", SPRITE_SCALING_PLANT)
        
            plant.x = randX
            plant.y = randY
            plant.level = 1
            plant.health = 10

            plantlist.append(plant)


            plant = arcade.Sprite("plant.jpg", SPRITE_SCALING_PLANT)
        
            plant.x = numSpacesX-randX
            plant.y = numSpacesY-randY
            plant.level = 1
            plant.health = 10

            plantlist.append(plant)
        
            plantCount = plantCount+2

            mapMatrix[randX][randY] = plantID
            mapMatrix[numSpacesX-1-randX][numSpacesY-1-randY] = plantID

def placeSlimes():
    # Set a given number of points in the matix to be plants spots
    print("Placing slimes")

    slimeCount = 0
    while slimeCount < numSlimes1+numSlimes2:
        randX = random.randint(0,numSpacesX/2-1)
        randY = random.randint(0,numSpacesY-1)
    
        #print(randX,randY)
    
        if mapMatrix[randX][randY] == 0:

            slime = arcade.Sprite("slime.jpg", SPRITE_SCALING_SLIME)
            slime.x = randX
            slime.y = randY
            slimelist1.append(slime)

            slime = arcade.Sprite("slime.jpg", SPRITE_SCALING_SLIME)
            slime.x = numSpacesX-randX
            slime.y = numSpacesY-randY
            slimelist2.append(slime)
        
            slimeCount +=2

            mapMatrix[randX][randY] = slimeID
            mapMatrix[numSpacesX-1-randX][numSpacesY-1-randY] = slimeID

class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "SlimeMind")


    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()
        
        arcade.set_background_color(arcade.color.ALMOND)

        StepY = (SCREEN_HEIGHT//(numSpacesY+2))
        StepX = (SCREEN_WIDTH//(numSpacesX+2))
        
        # Draw plants
        for i in range(numPlants):
            plantlist[i].center_x = (plantlist[i].x+1)*StepX
            plantlist[i].center_y = (plantlist[i].y+1)*StepY
            
            #print(plantlist[i].center_X,plantlist[i].center_Y)
            plantlist[i].draw()

            radius = (SCREEN_HEIGHT//numSpacesY)//4 * plantlist[i].level/10
            arcade.draw_circle_filled(plantlist[i].center_x, plantlist[i].center_y, radius, arcade.color.GREEN)

        # Draw slimes    
        for i in range(numSlimes1):
            slimelist1[i].center_x = (slimelist1[i].x+1)*StepX
            slimelist1[i].center_y = (slimelist1[i].y+1)*StepY
            radius = (SCREEN_HEIGHT//numSpacesY)//3
            arcade.draw_circle_filled(slimelist1[i].center_x, slimelist1[i].center_y, radius, arcade.color.BLUE)
            slimelist1[i].draw()

        for i in range(numSlimes2):
            slimelist2[i].center_x = (slimelist2[i].x+1)*StepX
            slimelist2[i].center_y = (slimelist2[i].y+1)*StepY
            radius = (SCREEN_HEIGHT//numSpacesY)//3
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
        for i in range(numPlants):
            UpgradeChance = random.randint(0,20)//1
            if UpgradeChance > plantlist[i].level:
                UpgradeChance = random.randint(0,20)//1
                if UpgradeChance > plantlist[i].level:
                    plantlist[i].level += 1
        
        # Call external function for slimes
        for i in range(numSlimes1):
            
            command = Player1.playerCommand(1)
            
            # Evaluate and exicute command
            if command == "up" and slimelist1[i].y < numSpacesY:
                slimelist1[i].y +=1
            if command == "down" and slimelist1[i].y > 0:
                slimelist1[i].y -=1
            if command == "right" and slimelist1[i].x < numSpacesX:
                slimelist1[i].x +=1
            if command == "left" and slimelist1[i].x >0:
                slimelist1[i].x -=1

        # Call external function for slimes
        for i in range(numSlimes2):
            
            command = Player2.playerCommand(1)
            
            # Evaluate and exicute command
            if command == "up" and slimelist2[i].y < numSpacesY:
                slimelist2[i].y +=1
            if command == "down" and slimelist2[i].y > 0:
                slimelist2[i].y -=1
            if command == "right" and slimelist2[i].x < numSpacesX:
                slimelist2[i].x +=1
            if command == "left" and slimelist2[i].x >0:
                slimelist2[i].x -=1

        # Delay to slow game down        
        time.sleep(0.1)

def main():
    makeMatrix()
    plantPlants()
    placeSlimes()
    MyGame()
    arcade.run()

if __name__ == "__main__":
    main()

