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
    def printPlayer(self):
        print("Player1")

class Player2(Tet):
    def printPlayer(self):
        print("Player2")

# Manually set constants

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600

SPRITE_SCALING_PLANT = 0.2
SPRITE_SCALING_SLIME = 0.15

numSpacesX = 30
numSpacesY = 15

plantID = 1
slimeID = 2

#Total number of plants
numPlants = 20

#Number of slimes per side
numSlimes1 = 2
numSlimes2 = 2


x = 0
y = 0
turn = 0

mapMatrix = []

plantList = arcade.SpriteList()
slimeList1 = arcade.SpriteList()
slimeList2 = arcade.SpriteList()

"""
plantList = [Plant() for i in range(numPlants)]
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

            plant = arcade.Sprite("plant.png", SPRITE_SCALING_PLANT)
        
            plant.x = randX
            plant.y = randY
            plant.level = 1
            plant.health = 10

            plantList.append(plant)


            plant = arcade.Sprite("plant.png", SPRITE_SCALING_PLANT)
        
            plant.x = numSpacesX-randX
            plant.y = numSpacesY-randY
            plant.level = 1
            plant.health = 10

            plantList.append(plant)
        
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

            slime = arcade.Sprite("slime.png", SPRITE_SCALING_SLIME)
            slime.x = randX
            slime.y = randY
            slimeList1.append(slime)

            slime = arcade.Sprite("slime.png", SPRITE_SCALING_SLIME)
            slime.x = numSpacesX-randX
            slime.y = numSpacesY-randY
            slimeList2.append(slime)
        
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
            plantList[i].center_x = (plantList[i].x+1)*StepX
            plantList[i].center_y = (plantList[i].y+1)*StepY
            radius = (SCREEN_HEIGHT//numSpacesY)//4 * plantList[i].level/10
            arcade.draw_circle_filled(plantList[i].center_x, plantList[i].center_y, radius, arcade.color.GREEN)
            plantList[i].draw()

        # Draw slimes    
        for i in range(numSlimes1):
            slimeList1[i].center_x = (slimeList1[i].x+1)*StepX
            slimeList1[i].center_y = (slimeList1[i].y+1)*StepY
            radius = (SCREEN_HEIGHT//numSpacesY)//3
            arcade.draw_circle_filled(slimeList1[i].center_x, slimeList1[i].center_y, radius, arcade.color.BLUE)
            slimeList1[i].draw()

        for i in range(numSlimes2):
            slimeList2[i].center_x = (slimeList2[i].x+1)*StepX
            slimeList2[i].center_y = (slimeList2[i].y+1)*StepY
            radius = (SCREEN_HEIGHT//numSpacesY)//3
            arcade.draw_circle_filled(slimeList2[i].center_x, slimeList2[i].center_y, radius, arcade.color.RED)
            slimeList2[i].draw()

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
            if UpgradeChance > plantList[i].level:
                UpgradeChance = random.randint(0,20)//1
                if UpgradeChance > plantList[i].level:
                    plantList[i].level += 1
        
        # Call external function for player 1 slimes
        for i in range(numSlimes1):
            
            command = Player1.playerCommand(1)
            
            # Evaluate and exicute command
            if command == "up" and slimeList1[i].y < numSpacesY:
                slimeList1[i].y +=1
            if command == "down" and slimeList1[i].y > 0:
                slimeList1[i].y -=1
            if command == "right" and slimeList1[i].x < numSpacesX:
                slimeList1[i].x +=1
            if command == "left" and slimeList1[i].x >0:
                slimeList1[i].x -=1
            
            # Check for collisions
            collision = 0
            for j in range(len(plantList)):
                if slimeList1[i].x == plantList[j].x and slimeList1[i].y == plantList[j].y:
                    collision = 1
            for j in range(len(slimeList1)):
                if slimeList1[i].x == slimeList1[j].x and slimeList1[i].y == slimeList1[j].y and not i == j:
                    collision = 1
            for j in range(len(slimeList2)):
                if slimeList1[i].x == slimeList2[j].x and slimeList1[i].y == slimeList2[j].y:
                    collision = 1

            # If there is a collision revert motion
            if collision:
                if command == "up" :
                    slimeList1[i].y -=1
                if command == "down":
                    slimeList1[i].y +=1
                if command == "right":
                    slimeList1[i].x -=1
                if command == "left":
                    slimeList1[i].x +=1

        # Call external function for player 2 slimes
        for i in range(numSlimes2):
            
            command = Player2.playerCommand(1)
            
            # Evaluate and exicute command
            if command == "up" and slimeList2[i].y < numSpacesY:
                slimeList2[i].y +=1
            if command == "down" and slimeList2[i].y > 0:
                slimeList2[i].y -=1
            if command == "right" and slimeList2[i].x < numSpacesX:
                slimeList2[i].x +=1
            if command == "left" and slimeList2[i].x >0:
                slimeList2[i].x -=1

            # Check for collisions
            collision = 0
            for j in range(len(plantList)):
                if slimeList2[i].x == plantList[j].x and slimeList2[i].y == plantList[j].y:
                    collision = 1
            for j in range(len(slimeList1)):
                if slimeList2[i].x == slimeList1[j].x and slimeList2[i].y == slimeList2[j].y and not i == j:
                    collision = 1
            for j in range(len(slimeList2)):
                if slimeList2[i].x == slimeList1[j].x and slimeList2[i].y == slimeList1[j].y:
                    collision = 1

            # If there is a collision revert motion
            if collision:
                if command == "up" :
                    slimeList2[i].y -=1
                if command == "down":
                    slimeList2[i].y +=1
                if command == "right":
                    slimeList2[i].x -=1
                if command == "left":
                    slimeList2[i].x +=1

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

