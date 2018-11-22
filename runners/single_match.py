from random import sample
from os import listdir
import importlib.util
from runners.runner_base import RunnerBase

class Runner(RunnerBase): 
    def __init__(self, player_dir):
        super().__init__("single_match", player_dir)

    def choose_players(self):
        """ randomly choose two unique players """
        players = [f for f in listdir(self.player_dir) if '.py' in f]
        file_one, file_two = sample(players, 2)
        print(file_one, "vs", file_two)

        spec = importlib.util.spec_from_file_location("PlayerCode.Player", self.player_dir + '/' + file_one)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        player_one = module.Player(1)

        spec = importlib.util.spec_from_file_location("PlayerCode.Player", self.player_dir + '/' + file_two)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        player_two = module.Player(2)

        return (player_one, player_two)

    def run(self):
        pass
