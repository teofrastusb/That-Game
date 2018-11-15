import arcade
import random
from models.plant import Plant

class Sprite_man():
    def __init__(self, plant_list, slimes_one, slimes_two):
        self.plant_list = plant_list
        self.slimes_one = slimes_one
        self.slimes_two = slimes_two

    def update(self):
        # nothin to do...yet
        pass

    def check_for_dead(self,mapthing):
        #print('Bring out your dead!')
        self.kill_list = []

        for plant in self.plant_list:
            if plant.current_hp <= 0:
                self.kill_list.append(plant)

        for slime in self.slimes_one:
            if slime.current_hp <= 0:
                self.kill_list.append(slime)

        for slime in self.slimes_two:
            if slime.current_hp <= 0:
                self.kill_list.append(slime)


        for gamepiece in self.kill_list:
            arcade.sprite.Sprite.kill(gamepiece) 
            mapthing.clear_cell(gamepiece.x,gamepiece.y)

    def spread_seeds(self,mapthing,all_sprites_list,conf):
        #In spread seeds
        to_plant =[]
        for planter in self.plant_list:
            if planter.seed:
                to_plant.append(planter)

        giveup = 0
        for planter in to_plant:
            can_plant = False
            while not can_plant and giveup <= 5:
                option = random.randint(0,3)
                
                if option == 0:
                    dx = 1
                    dy = 0
                elif option == 1:
                    dx = -1
                    dy = 0
                elif option == 2:
                    dx = 0
                    dy = 1
                elif option == 3:
                    dx = 0
                    dy = -1

                if not(planter.x+dx is -1 or planter.x+dx is mapthing.column_count() or 
                    planter.y+dy is -1 or planter.y+dy is mapthing.row_count()):
                    if mapthing.matrix[planter.x+dx][planter.y+dy] == 0:
                        can_plant = True
                    else:
                        giveup += 1

            if can_plant:
                plant = Plant('this is from can_plant', conf, mapthing)
                plant.set_coord(planter.x+dx,planter.y+dy)
                all_sprites_list.append(plant)
                self.plant_list.append(plant)
                planter.seed = False    
