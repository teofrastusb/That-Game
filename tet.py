#!/usr/bin/env python
#This will passback movement directons to the slimes
class Tet():  

    def playerCommand(self):
        # Setup an empty matrix of the correct size
        moveList = ["left", "right","up","down"]
        import random 
        command = random.randint(0,3)
        command = moveList[command]
        return command
