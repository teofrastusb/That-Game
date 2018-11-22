import logging
import configparser
import importlib.util

class RunnerBase(): 
    def __init__(self, name, player_dir):
        self.name = name
        self.player_dir = player_dir
        self.config = configparser.ConfigParser()
        self.config.read('resources/config.ini')

        # setup logging
        logger = logging.getLogger()
        logger.setLevel(self.config['logging']['level'])
        logger.addHandler(logging.StreamHandler())

    def create_player(self, filename, player_num):
        spec = importlib.util.spec_from_file_location("PlayerCode.Player", self.player_dir + '/' + filename)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.Player(player_num)

    def run(self):
        raise NotImplementedError("All runners must implement this method")

    def choose_players(self):
        raise NotImplementedError("All runners must implement this method")