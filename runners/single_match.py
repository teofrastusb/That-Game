import arcade
from random import sample
from os import listdir

from runners.runner_base import RunnerBase
from engine.engine import Engine
from visualizer.visualizer import Visualizer

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

        engine = Engine(self.config, player_one, player_two)

        # visualize or just run the match
        if self.config['visualizer'].getboolean('render'):
            visualizer = Visualizer(self.config, engine.map.dump_state(), engine.run_turn, player_one.name, player_two.name)
            arcade.window_commands.run()
        else:
            while not engine.is_game_over():
                engine.run_turn()

        results = engine.end_game()
        self.record_results(results)
