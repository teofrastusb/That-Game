import arcade

class Sprite_man():
    def __init__(self, plant_list, slimes_one, slimes_two):
        self.plant_list = plant_list
        self.slimes_one = slimes_one
        self.slimes_two = slimes_two

    def update(self):
        # nothin to do...yet
        pass

    def check_for_dead(self):
        # Bring out your dead!
        self.kill_list = []

        for plant in self.plant_list:
            if plant.current_hp == 0:
                self.kill_list.append(plant)

        for slime in self.slimes_one:
            if slime.current_hp == 0:
                self.kill_list.append(slime)

        for slime in self.slimes_two:
            if slime.current_hp == 0:
                self.kill_list.append(slime)

        """
        for gamepiece in self.kill_list:
            self.kill(gamepiece)
        """
