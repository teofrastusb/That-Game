import arcade

class Sprite_man():
    def __init__(self, id, config, map):

        self.id = id
        self.map = map


    def update(self):
        # nothin to do...yet
        pass

    def check_for_dead(self):
        # Bring out your dead!
        self.kill_list = []

        for plant in self.plant_list:
            if plant.hp == 0
                self.kill_list.append(plant)
                
        self.plant_list = arcade.SpriteList()
        self.slimes_one = arcade.SpriteList()
        self.slimes_two = arcade.SpriteList()
        self.all_sprites_list = arcade.SpriteList()