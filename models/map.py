import copy

class Map():
    def __init__(self, config):
        self.width = config['screen'].getint('width')
        self.height = config['screen'].getint('height') 
        self.rows = config['screen'].getint('rows')
        self.columns = config['screen'].getint('columns')
        self.matrix = [[0]*config['screen'].getint('columns') for i in range(config['screen'].getint('rows'))]
        self.margin = 2

    def get_matrix(self):
      return self.matrix
    
    def row_count(self):
      return self.rows

    def column_count(self):
      return self.columns

    def step_x(self):
      return self.width // (self.rows + self.margin)
    
    def step_y(self):
      return self.height // (self.columns + self.margin)