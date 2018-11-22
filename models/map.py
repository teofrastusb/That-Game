class Map():
    def __init__(self, config):
        self.width = config['screen'].getint('width')
        self.height = config['screen'].getint('height') 
        self.rows = config['screen'].getint('rows')
        self.columns = config['screen'].getint('columns')
        # This setup creates a matrix with [x][y] coordinates even though it looks backwards
        self.matrix = [[None] * config['screen'].getint('rows') for i in range(config['screen'].getint('columns'))]
        self.margin = 2
        self.step_x = self.width // (self.columns)
        self.step_y = self.height // (self.rows)

    def adjacent_cells(self, x, y):
      cells = [
        (x - 1, y),
        (x, y -1),
        (x - 1, y - 1),
        (x + 1, y),
        (x, y + 1),
        (x + 1, y + 1),
        (x - 1, y + 1),
        (x + 1, y - 1)
      ]
      return [cell for cell in cells if self.valid_coord(cell[0], cell[1])] 

    def move_gamepiece(self, gamepiece, x, y):
      # clear original, if occupied
      self.clear_cell(gamepiece.x, gamepiece.y)

      # move to new spot
      gamepiece.x = x
      gamepiece.y = y
      self.update_cell(gamepiece, x, y)

      # display
      gamepiece.set_position(self.center_x(x), self.center_y(y))

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

    def is_cell_empty(self, x, y):
      return self.matrix[x][y] == None

    def adjacent_empty_cells(self, x, y):
      cells = self.adjacent_cells(x, y)
      return [(x, y) for x, y in cells if self.is_cell_empty(x, y)]

    def valid_coord(self, x, y):
      return (x is not None and y is not None and (0 <= x < self.columns) and (0 <= y < self.rows))

    def update_cell(self, gamepiece, x, y):
      if self.is_cell_empty(x, y):
        self.matrix[x][y] = gamepiece

    def clear_cell(self, x, y):
      if self.valid_coord(x, y):
        self.matrix[x][y] = None

    def dump_state(self):
      state = [[None] * self.rows for i in range(self.columns)]
      for x in range(len(self.matrix)):
        for y in range(len(self.matrix[x])):
          piece = self.matrix[x][y]
          if piece is not None:
            state[x][y] = piece.__dict__()
      return state