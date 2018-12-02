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

# Game Pieces
There are three types of game piece in this game. All of them are given the following attributes:
```
x - This is the column index of the game piece (starting from 0)
y - This is the row index of the game piece (starting from 0)
```

### Rocks
Rocks are only meant to get in the way. They are placed at the beginning of the game and cannot be moved or destroyed.

### Plants
Plants are the food source for the slimes. All plants have the following attributes:
```
max_level - This is the highest level a plant can reach.
level - Used to calculate the maximum health of the plant. 
max_hp - This is the most health a plant can have.
current_hp - This is the current health of a plant.
```
Plants are placed at the beginning of the game at level 1 with a set amount of health. Every round the plant has a % chance to level up determined by a random number generation. If the plant does level up it will gain health and maximum health based on its level. Once a plant reaches its maximum level it will gain the ability to spread seeds. Every round a max level plant has a % chance to spread a seed to one of the 8 squares surrounding it. If a plant succeeds in seeding another plant at level 1 will be placed in the target square. Plants at maximum level will change color in the visulizer. 

### Slimes
Slimes are the gamepieces controlled by the submitted AI code and will be used to determine which code wins a game. Each slime has the following attributes:
```
xp - Used to calculate the level of a slime.
max_level - This is the highest level a slime can reach.
level - Used to calculate the attack and maximum health of the slime. 
maximum_hp - This is the most health a slime can have.
current_hp - This is the current health of a slime.
attack -  This is the amount of health a slime or plant will lose when this slime bites it.
```
Slimes are placed at the beginning of the game at level 1. Each round a given slime will update based on its xp to adjust to its correct level, and adjust its attack and max_hp based on the slimes level.  The tabel below shows the minimum xp for a slime to become each level and the other attributes for that level. The full equation can be found in the code.
```
xp	level	attack	max_hp
1	1	3	11
2	2	4	13
6	3	7	17
15	4	10	22
33	5	13	28
62	6	16	35
106	7	20	43
169	8	24	52
254	9	29	62
368	10	33	73
513	11	38	84
695	12	43	97

```
Next the slime will call it's team's submitted AI code and wait a a maximum of a set amount of time to recive one of the approved commands discussed in the next section. If no command is returned in that amount of time the round is skipped and the next slime is called. If a valid command is returned then the slime will attempt to prefrom whatever command has been submitted. Finally at the end of every slimes round the game code will check for any slimes or plants that have had their current_hp dropped to or below 0 and remove them from the game.

# Commands
There are only 10 acceptable commands that a slime can accept. They are:
```
LEFT
RIGHT
UP
DOWN
BITELEFT
BITERIGHT
BITEUP
BITEDOWN
SPLIT
MERGE
```
Anything else retuned from an AI code besides these options including changes to the game state (such as setting all slimes to max level) will result in the slime losing its round.

### Move Commands
The four move commands availble to the slimes are:
```
LEFT
RIGHT
UP
DOWN
```
When given any of these commands the game code will attempt to move the slime to the square in the corresponding direction (Left moves the slime to the square that has the same y value but an x value of one less ect.). However if the traget square is occupied by another game piece or is past the edge of the map then the slime will do nothing during its round.

### Bite Commands
The four bite commands availble to the slimes are:
```
BITELEFT
BITERIGHT
BITEUP
BITEDOWN
```
When given any of these commands the game code will check to see if a valid target is located in the corresponding location (same logic as for the move commands). If there is not a valid target in the location then the slime will do nothing for its round. If there is a slime or plant object in the target location then that slime or plant will have its current_health reduced by the biting slimes attack value. The bitting slime will also have its current_hp inceased by 1 and its xp increased by 1.

### Split Command
The only split command availble to the slimes is:
```
SPLIT
```
When given this command the game code will check to see if the slime is at least level 4. The code will then check to see if there is an emptey space adjacent to the slime. If both criteria are met then the slime will have its xp divided by 4 to the nearest integer and another level 1 slime is created in a randome empty adjacent space. 

### Merge Commands
The only merge command availble to the slimes is:
```
MERGE
```
When given this command the game code will set the slime as ready to merge. The code will then check to see if there are any friendly slimes in adjacent squares that are ready to set as ready to merge. If an adjacent slime is found then it will be destroyed and the destroyed slimes xp will be added to the xp of the initiating slime. At the beginning of its round a slime will have its ready to merge status removed.


# Victory conditions
The game will continue until turn 1000 is complete or until no slimes for one team is destroyed. Once the game is completed then the score for each team is calculated using the remaining slimes. This score calculation is detailed in the code and is based soley on the slimes level not on its total xp. The tabel below shows a simplified level to score ratio. The full equation can be found in the code.
```
level	points
1	0.2
2	0.4
3	1.6
4	5.2
5	13.7
6	29.9
7	57.7
8	101.7
9	167.0
10	259.7
11	386.7
12	555.3

```
The team with the most total points at the end of the game wins.

# Writing a Custom AI
Every writer should use the supplied player_base.py to make there own code. Blah blah compete with people yadda yadda programing.
### Use player_base.py

# Sprites
Each team will currently need two sprites to run.

### Standard sprites
For now the only option is to use the standard sprites provided with the game program.

### Adding Custom sprites
In the near future the ability to load custom sprites will be added. The sprites will need to be .png and have transparent backgrounds. They should also be square other then that there should be no limit on the images size.

The files will need to be submitted with specific names TBD

### Possible future options
If there is intrest additional sprites may be added to show each time a slime levels up (or maybe every other time).




