import copy

class Map():
    def __init__(self, config):
        self.width = config['screen'].getint('width')
        self.height = config['screen'].getint('height') 
        self.rows = config['screen'].getint('rows')
        self.columns = config['screen'].getint('columns')
        self.matrix = [[0] * config['screen'].getint('columns') for i in range(config['screen'].getint('rows'))]
        self.margin = 2
        self.step_x = self.width // (self.rows + self.margin)
        self.step_y = self.height // (self.columns + self.margin)

    def get_matrix(self):
      return self.matrix
    
    def row_count(self):
      return self.rows

    def column_count(self):
      return self.columns

    def center_x(self, x):
      return (x + 1) * self.step_x
    
    def center_y(self, y):
      return (y + 1) * self.step_y

    def cell_empty(self, x, y):
      return self.matrix[x][y] == 0
    
    def update_cell(self, gamepiece, x, y):
      if self.cell_empty(x, y):
        self.matrix[x][y] = gamepiece

    def clear_cell(self, x, y):
      self.matrix[x][y] = 0