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
NumSpacesX = 30
NumSpacesY = 10

PlantID = 1
NumPlants = 20
NumSlimes = 2

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600

x = 0
y = 0
turn = 0

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
plantlist = [Plant() for i in range(NumPlants)]

def makeMatrix():
    # Setup an empty matrix of the correct size
    MapArray = []

    for i in range(NumSpacesX):
        MapArray.append([0]*NumSpacesY)
        
    return MapArray

def plantPlants(MapArray):
    # Set a given number of points in the matix to be plants spots
    PlantCount = 0
    while PlantCount < NumPlants:
        randX = random.randint(0,NumSpacesX/2-1)
        randY = random.randint(0,NumSpacesY-1)
    
        #print(randX,randY)
    
        if MapArray[randX][randY] == 0:
        
            plantlist[PlantCount].x = randX
            plantlist[PlantCount].y = randY
        
            plantlist[PlantCount+1].x = NumSpacesX-randX
            plantlist[PlantCount+1].y = NumSpacesY-randY
        
            PlantCount = PlantCount+2

            MapArray[randX][randY] = PlantID
            MapArray[NumSpacesX-1-randX][NumSpacesY-1-randY] = PlantID 

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

        StepY = (SCREEN_HEIGHT//(NumSpacesY+2))
        StepX = (SCREEN_WIDTH//(NumSpacesX+2))

        for i in range(NumPlants):
            x = (plantlist[i].x+1)*StepX
            y = (plantlist[i].y+1)*StepY
            radius = (SCREEN_HEIGHT//NumSpacesY)//4 * plantlist[i].level/10
            arcade.draw_circle_filled(x, y, radius, arcade.color.GREEN)

        # Put the text on the screen.
        output = "turn: {}".format(turn)
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    def update(self, delta_time):
        """ Movement and game logic """
        UpgradeChance = 0
        
        global turn
        turn += 1
        
        for i in range(NumPlants):
            UpgradeChance = random.randint(0,20)//1
            if UpgradeChance > plantlist[i].level:
                plantlist[i].level += 1
                print(plantlist[i].level)
                
        time.sleep(0.1)



def main():
    MapArray = makeMatrix()
    plantPlants(MapArray)
    MyGame()
    arcade.run()

if __name__ == "__main__":
    main()

