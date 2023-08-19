class Cell():
  value: int = None
  row = None
  col = None
  group = None

  def __init__(self, index):
    self.options = [x + 1 for x in range(9)]
    self.index = index

  def set_value(self, value: int):
    print(f'Cell[{self.index}] -> {value}')
    self.value = value
    self.options = []
    # iterate the rows/columns/groups and remove impossible options
    self.row.remove_option(value)
    self.col.remove_option(value)
    self.group.remove_option(value)

  def set_row(self, row):
    self.row = row

  def set_col(self, col):
    self.col = col

  def set_group(self, group):
    self.group = group

  def remove_option(self, value):
    if self.value is None:
      if value in self.options:
        old_options = self.options.copy()
        self.options.remove(value)
        print(f'Cell[{self.index}] {old_options} -> {self.options}')
      if len(self.options) == 1:
        print(f'Found single entry option list for cell [{self.index}]')
        self.set_value(self.options[0])

  def __str__(self):
    if self.value is None:
      return str(self.options)
    return str(self.value)


class Row():
  cells = []

  def __init__(self, cells):
    #print(args)
    if not len(cells) == 9:
      raise ValueError(
        ValueError(f'9 arguments expected for a row, {cells} received'))
    self.cells = cells
    for cell in self.cells:
      cell.set_row(self)

  def remove_option(self, value):
    for cell in self.cells:
      cell.remove_option(value)

  def __str__(self):
    return ','.join([str(x) for x in self.cells])


class Col():
  cells = []

  def __init__(self, cells):
    #print(args)
    if not len(cells) == 9:
      raise ValueError(
        ValueError(f'9 arguments expected for a column, {cells} received'))
    self.cells = cells
    for cell in self.cells:
      cell.set_col(self)

  def remove_option(self, value):
    for cell in self.cells:
      cell.remove_option(value)

  def __str__(self):
    return ','.join([str(x) for x in self.cells])


class Group():
  cells = []

  def __init__(self, cells):
    #print(args)
    if not len(cells) == 9:
      raise ValueError(
        ValueError(f'9 arguments expected for a group, {cells} received'))
    self.cells = cells
    for cell in self.cells:
      cell.set_group(self)

  def remove_option(self, value):
    for cell in self.cells:
      cell.remove_option(value)

  def __str__(self):
    return ','.join([str(x) for x in self.cells])


class Grid():

  def __init__(self, *args):
    # setup the grid with None's first
    self.cells = [Cell(x) for x in range(len(args))]

    # Create rows
    self.rows = [
      Row(self.cells[i:i + 9]) for i in range(0, len(self.cells), 9)
    ]

    # Create cols
    ranges = [range(i, 81, 9) for i in range(9)]
    self.cols = []
    for r in ranges:
      col = Col([self.cells[x] for x in r])
      self.cols.append(col)

    rr = [range(x, x + 9, 3) for x in [0, 27, 54]]
    self.groups = []
    for r in rr:
      for ii in r:
        indices = [
          ii, ii + 1, ii + 2, ii + 9, ii + 10, ii + 11, ii + 18, ii + 19,
          ii + 20
        ]
        group = Group([self.cells[x] for x in indices])
        self.groups.append(group)

    for ii in range(len(args)):
      if not args[ii] is None:
        self.cells[ii].set_value(args[ii])

  def __str__(self):
    return '|' + '|\n|'.join([str(x) for x in self.rows]) + '|'


if __name__ == '__main__':
  # Create the grid
  g = Grid(None, 7, None, 1, None, 5, None, 4, None, 6, None, 4, 9, None, 2, 5,
           None, 1, None, 1, None, 6, None, 4, None, 3, None, 4, 2, 8, None,
           None, None, 1, 7, 6, None, None, None, None, None, None, None, None,
           None, 7, 6, 9, None, None, None, 3, 5, 4, None, 4, None, 3, None, 7,
           None, 2, None, 2, None, 1, 4, None, 9, 7, None, 3, None, 9, None, 2,
           None, 8, None, 1, None)
  print(g)

