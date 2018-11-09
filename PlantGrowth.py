#!/usr/bin/env python

"""
This program will attempt to set the plants to grow.
"""

# Import as needed
import arcade
import random
import os
import time

# Manually set constants
numSpacesX = 30
numSpacesY = 10

plantID = 1
slimeID = 2
numPlants = 20
numSlimes = 2

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600

x = 0
y = 0
turn = 0

mapMatrix = []
# Setup classes for needed objects
class Plant:
    """
    Class to keep track of a plant's location, level, and health.
    """
    x = 0
    y = 0
    level = 1
    health = 10

class Slime:
    """
    Class to keep track of a plant's location, level, and health.
    """
    x = 0
    y = 0
    level = 1
    health = 5
    attack = 5
    xp = 0

# Global list
plantlist = [Plant() for i in range(numPlants)]
slimelist = [Slime() for i in range(numSlimes)]

def makeMatrix():
    # Setup an empty matrix of the correct size

    for i in range(numSpacesX):
        mapMatrix.append([0]*numSpacesY)
        


def plantPlants():
    # Set a given number of points in the matix to be plants spots
    PlantCount = 0
    while PlantCount < numPlants:
        randX = random.randint(0,numSpacesX/2-1)
        randY = random.randint(0,numSpacesY-1)
    
        #print(randX,randY)
    
        if mapMatrix[randX][randY] == 0:
        
            plantlist[PlantCount].x = randX
            plantlist[PlantCount].y = randY
        
            plantlist[PlantCount+1].x = numSpacesX-randX
            plantlist[PlantCount+1].y = numSpacesY-randY
        
            PlantCount = PlantCount+2

            mapMatrix[randX][randY] = plantID
            mapMatrix[numSpacesX-1-randX][numSpacesY-1-randY] = plantID

                
            
def placeSlimes():
    # Set a given number of points in the matix to be plants spots
    slimeCount = 0
    while slimeCount < numSlimes:
        randX = random.randint(0,numSpacesX/2-1)
        randY = random.randint(0,numSpacesY-1)
    
        #print(randX,randY)
    
        if mapMatrix[randX][randY] == 0:
        
            slimelist[slimeCount].x = randX
            slimelist[slimeCount].y = randY
        
            slimelist[slimeCount+1].x = numSpacesX-randX
            slimelist[slimeCount+1].y = numSpacesY-randY
        
            slimeCount +=2
            print(numSlimes,slimeCount)

            mapMatrix[randX][randY] = slimeID
            mapMatrix[numSpacesX-1-randX][numSpacesY-1-randY] = slimeID

class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Basics")


    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()
        
        arcade.set_background_color(arcade.color.ALMOND)

        StepY = (SCREEN_HEIGHT//(numSpacesY+2))
        StepX = (SCREEN_WIDTH//(numSpacesX+2))

        for i in range(numPlants):
            x = (plantlist[i].x+1)*StepX
            y = (plantlist[i].y+1)*StepY
            radius = (SCREEN_HEIGHT//numSpacesY)//4 * plantlist[i].level/10
            arcade.draw_circle_filled(x, y, radius, arcade.color.GREEN)
            
        for i in range(numSlimes):
            x = (slimelist[i].x+1)*StepX
            y = (slimelist[i].y+1)*StepY
            radius = (SCREEN_HEIGHT//numSpacesY)//3
            arcade.draw_circle_filled(x, y, radius, arcade.color.BLUE)

        # Put the text on the screen.
        output = "turn: {}".format(turn)
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    def update(self, delta_time):
        """ Movement and game logic """
        UpgradeChance = 0
        
        global turn
        turn += 1
        
        for i in range(numPlants):
            UpgradeChance = random.randint(0,20)//1
            if UpgradeChance > plantlist[i].level:
                plantlist[i].level += 1
                print(plantlist[i].level)
                
        time.sleep(0.1)



def main():
    makeMatrix()
    print(1)
    plantPlants()
    print(2)
    placeSlimes()
    print(3)
    MyGame()
    arcade.run()

if __name__ == "__main__":
    main()

