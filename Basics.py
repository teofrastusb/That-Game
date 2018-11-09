#!/usr/bin/env python

"""
This program will attempt to setup a matrix to hold track the gameboard squares, generate locations to put plants, and draw the game board.
"""

# Import as needed
import arcade
import random
import os

# Manually set constants
NumSpacesX = 30
NumSpacesY = 10

PlantID = 1
NumPlants = 20

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600

# Setup classes for needed objects
class Plant:
    """
    Class to keep track of a plant's location, level, and health.
    """
    x = 0
    y = 0
    level = 1
    health = 10
        
plantlist = [Plant() for i in range(NumPlants)]

# Setup an empty matrix of the correct size
MapArray = []

for i in range(NumSpacesX):
    MapArray.append([0]*NumSpacesY)

print(MapArray)

# Set a given number of points in the matix to be plants spots
PlantCount = 0
while PlantCount < NumPlants:
    randX = random.randint(1,NumSpacesX/2)
    randY = random.randint(1,NumSpacesY)
    
    print(randX)
    print(randY)
    
    if MapArray[randX][randY] == 0:
        
        plantlist[PlantCount].x = randX
        plantlist[PlantCount].y = randY
        
        plantlist[PlantCount+1].x = NumSpacesX-randX
        plantlist[PlantCount+1].Y = NumSpacesY-randY
        
        PlantCount = PlantCount+2

        MapArray[randX][randY] = PlantID
        MapArray[NumSpacesX-randX][NumSpacesY-randY] = PlantID 

# Draw the gameboard with the plants

# Open the window. Set the window title and dimensions (width and height)
arcade.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Basics")

# Set the background color to white.
# For a list of named colors see:
# http://arcade.academy/arcade.color.html
# Colors can also be specified in (red, green, blue) format and
# (red, green, blue, alpha) format.
arcade.set_background_color(arcade.color.ALMOND)
# Draw the plant according to the matrix
x = 0
y = 0
radius = (SCREEN_HEIGHT//NumSpacesY)//4

StepY = (SCREEN_HEIGHT//(NumSpacesY+1))
StepX = (SCREEN_WIDTH//(NumSpacesX+1))

for i in range(NumSpacesX):
    for j in range(NumSpacesY):
        if MapArray[i][j] == 1:
            x = StepX*(1+i)
            y = StepY*(1+j)
            arcade.draw_circle_filled(x, y, radius, arcade.color.GREEN)

# Finish drawing and display the result
arcade.finish_render()

# Keep the window open until the user hits the 'close' button
arcade.run()

