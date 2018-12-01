# Slime Mind

![this shows if it can't load](images/slime_blue.png "This shows on hover")

# Introduction
We made this game structure to allow us to write and test AI programs. Each writer will be given a main.py, some example AI codes, and some support .py codes. Writers can use the example code to explore making thier own codes and to run against. As a writer's code  advances they should submit it to be tested against other writers' codes. Evenutally tournaments will be run between all submissions. 

The current game is still being balanced and many of the parameters will likely be changed. Changes will be made in an attempt to balance the system but not destroy certain stratagies. If someone figures out a way to win no matter what through complex codeing or an out of the box stratgy then good for them.

Eventually additional game mechanics may be added, and a new game with the same basic structure but additional mechanics may be released.
  
# Setup
### Suggested IDE
There are many programs or tools that can be used to write programs in the python language. 
One such program is Visual Studio Code (https://code.visualstudio.com/), you will need at least one
of these programs to install python and create your custom AIs.

### Installing python
https://code.visualstudio.com/docs/languages/python

You will need to install python using your IDE.


### Installing libraries
Python libraries that must be included to run the game are listed below. You are not limited to only these libraries but if you call any outside of this list in you code please be sure to note that in your submissions.
```
arcade
random
time
argparse
math
logging
os
concurrent.futures
```
# Custom Programs
### Where to Get
Ian we need to discuss how people will get these programs. I'm cool with them pulling from the github but I worry that too many people with write acess will lead to mistakes that we may have to go in a fix.
### List of Main Programs
```
main.py
replay.py
player_base.py
player_one.py
player_two.py
player_three.py
```
### Folder Structure
There must be the following folder structure to run main.py
```
Slime Mind
  engine
  images
  models
  playerCode
  resources
  runners
  timer
  viualizer
  main.py
 ```
### Running a Match
To run a single match run the following code in the terminal commmand line: 
```
python main.py
```
This will run a match between two randomly selected codes in the playerCode folder.


To run multiple matches in a row run the follwing code to explain the needed inputs:
```
python main.py --help
```
the final command to run multiple matches should look similar to this.
```
python main.py -r multi_match -m 100 -1 player_four.py -2 player_three.py
```
be sure to turn off the visulizer by setting the render boolean varialbe in the config.py file to 0 before running multiple matches.

### Replaying a Match

# Game mechanics
### Game explination
Slime Mind is played on a map that is broken into squares with a set number of columns and rows. The exact number of columns and rows may be changed in the config.py file. However the standard number that will be used for tournaments and such is:
30 columns and 15 rows (likely this will be tweaked).
At the start of a game plants, stones, and slimes are put randomly on the map with another of the same object being placed in a location that is mirroed across both the x and y axis. The slimes will be broken into teams based on their starting locations. Each team will use on of the loaded AI codes.
Once a game begins each object will be given a single round per turn. 
Rocks go first and do nothing.
Plants will go next and run on a defined AI described in the Game Pieces section of this document.
Slimes will then go alternating between each team until all slimes have gone.
Then the map will update and the turn will be completed.

### Game Pieces
There are three types of game piece in this game.

Rocks - Are placed at the beginning of the game and cannot be moved or destroyed.

Plants - Are placed at the beginning of the game at level 1 with a set amount of health. Every round the plant has a % chance to level up determined by a random number generation. If the plant does level up it will gain health and maximum health based on its level. Once a plant reaches its maximum level it will gain the ability to spread seeds. Every round a max level plant has a % chance to spread a seed to one of the 8 squares surrounding it. If a plant succeeds in seeding another plant at level 1 will be placed in the target square.
Plants at maximum level will change color in the visulizer.

### Victory conditions
### Commands

# Writing a Custom AI
### Use player_base.py

# Sprites
### Standard sprites
### Adding Custom sprites
### Possible future options





