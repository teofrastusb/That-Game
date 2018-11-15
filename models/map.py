import copy

class Map():
    def __init__(self, config):
        self.width = config['screen'].getint('width')
        self.height = config['screen'].getint('height') 
        self.rows = config['screen'].getint('rows')
        self.columns = config['screen'].getint('columns')
        # This setup creates a matrix with [x][y] coordinates even though it looks backwards
        self.matrix = [[0] * config['screen'].getint('rows') for i in range(config['screen'].getint('columns'))]
        self.margin = 2
        self.step_x = self.width // (self.columns)
        self.step_y = self.height // (self.rows)

    def get_matrix(self):
      return self.matrix
    
    def row_count(self):
      return self.rows

    def column_count(self):
      return self.columns

    def center_x(self, x):
      return (x + 1/2) * self.step_x
    
    def center_y(self, y):
      return (y + 1/2) * self.step_y

    def cell_empty(self, x, y):
      return self.matrix[x][y] == 0

    def adjacent_cells(self, x, y):
      return [
        (x - 1, y),
        (x, y -1),
        (x - 1, y - 1),
        (x + 1, y),
        (x, y + 1),
        (x + 1, y + 1),
        (x - 1, y + 1),
        (x + 1, y - 1)
      ]

    def valid_coord(self, x, y):
      return ((0 <= x < self.columns) and (0 <= y < self.rows))

    def update_cell(self, gamepiece, x, y):
      if self.cell_empty(x, y):
        self.matrix[x][y] = gamepiece

    def clear_cell(self, x, y):
      self.matrix[x][y] = 0