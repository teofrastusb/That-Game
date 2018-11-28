import arcade
from random import sample
from os import listdir

from runners.runner_base import RunnerBase
from visualizer.visualizer import Visualizer
from timer.timer import timed
class Runner(RunnerBase): 
    def __init__(self, player_dir, filename):
        super().__init__("visualize_recording", player_dir)
        with open(filename, 'r') as f:
            self.recording = f.readlines()
        self.i = 0

    def next_state(self):
        data = False
        if self.i < len(self.recording):
            data = eval(self.recording[self.i])
        self.i+= 1
        return data

    def run(self):
        visualizer = Visualizer(self.config, self.next_state(), self.next_state)
        timed(arcade.window_commands.run)()