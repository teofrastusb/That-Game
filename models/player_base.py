import random
from models.commands import Commands

class PlayerBase():
    def __init__(self):
        self.commands = Commands

    def command_slime(self, map, slime):
        """
          Player's should override this method to provide an AI for each slime they control.
          They must return a Command for the slime to take.
          Invalid or impossible commands (e.g. moving onto a taken coordinate or eating nothing) will be ignored.
        """
        # default implementation is a random selection from all commands
        return random.choice(list(self.commands))