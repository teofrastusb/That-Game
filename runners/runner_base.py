class RunnerBase(): 
    def __init__(self, name, player_dir):
        self.name = name
        self.player_dir = player_dir
        self.filename = name + '_results.csv'

    def record_results(self, results):
        """ Generate report, ... """
        existing_file = os.path.isfile(self.filename)
        with open(self.filename, 'a', newline = '') as f:
            writer = csv.DictWriter(f, fieldnames = results.keys())
            if not existing_file:
                writer.writeheader()
            writer.writerow(results)

    def run(self):
        raise NotImplementedError("All runners must implement this method")

    def choose_players(self):
        raise NotImplementedError("All runners must implement this method")