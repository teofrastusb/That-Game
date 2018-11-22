import arcade
from random import sample
from os import listdir

from runners.runner_base import RunnerBase
from engine import Engine

class Runner(RunnerBase): 
    def __init__(self, player_dir):
        super().__init__("single_match", player_dir)

    def choose_players(self):
        """ randomly choose two unique players """
        players = [f for f in listdir(self.player_dir) if '.py' in f]
        file_one, file_two = sample(players, 2)
        print(file_one, "vs", file_two)

        player_one = self.create_player(file_one, 1)
        player_two = self.create_player(file_two, 2)

        return (player_one, player_two)

    def run(self):
        player_one, player_two = self.choose_players()

        # run the actual game
        window = Engine(self.config, player_one, player_two)
        arcade.run()
