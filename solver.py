import csv
import math


class Tracer:
    def __init__(self):
        pass

    @staticmethod
    def trace(cell, msg):
        print(f'[{cell.i},{cell.j}]: {msg}')


tracer = Tracer()


class Cell:
    value: int = 0
    row = None
    col = None
    group = None

    def __init__(self, index):
        self.options = [x + 1 for x in range(9)]
        self.index = index
        self.i = math.floor(index / 9)
        self.j = index % 9

    def set_value(self, value: int, reason:  str):
        tracer.trace(self, f'-> {value} [{reason}]')
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
        if self.value == 0:
            if value in self.options:
                old_options = self.options.copy()
                self.options.remove(value)
                tracer.trace(self, f'{old_options} -> {self.options}')

    def __str__(self):
        if self.value == 0:
            return '(' + ';'.join([str(x) for x in self.options]) + ')'
        return str(self.value)


class Row:
    cells = []

    def __init__(self, cells):
        # print(args)
        if not len(cells) == 9:
            raise ValueError(
                ValueError(f'9 arguments expected for a row, {cells} received'))
        self.cells = cells
        for cell in self.cells:
            cell.set_row(self)

    def remove_option(self, value):
        for cell in self.cells:
            cell.remove_option(value)

    def group_str(self, start, end):
        return ','.join([str(x) for x in self.cells[start:end]])

    def __str__(self):
        g1 = self.group_str(0, 3)
        g2 = self.group_str(3, 6)
        g3 = self.group_str(6, 9)
        return f'|{g1}|{g2}|{g3}|'


class Col:
    cells = []

    def __init__(self, cells):
        # print(args)
        if not len(cells) == 9:
            raise ValueError(
                ValueError(f'9 arguments expected for a column, {cells} received'))
        self.cells = cells
        for cell in self.cells:
            cell.set_col(self)

    def remove_option(self, value):
        for cell in self.cells:
            cell.remove_option(value)
        # find indices of each number
        indices = {}
        for ii in range(1, 10):
            for cell in self.cells:
                if ii in cell.options:
                    if ii not in indices:
                        indices[ii] = []
                    indices[ii].append(cell)

    def __str__(self):
        return ','.join([str(x) for x in self.cells])


class Group:
    cells = []

    def __init__(self, cells):
        # print(args)
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


class Grid:

    def __init__(self, args):
        # setup the empty grid first
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
                    ii, ii + 1, ii + 2, ii + 9, ii + 10, ii + 11, ii + 18, ii + 19, ii + 20
                ]
                group = Group([self.cells[x] for x in indices])
                self.groups.append(group)

        for ii in range(len(args)):
            if not args[ii] == 0:
                self.cells[ii].set_value(args[ii], 'Initial')
    
    def solve(self):
        updated = False
        # cells which have only one option
        for cell in self.cells:
            if len(cell.options) == 1:
                cell.set_value(cell.options[0], 'only option')
                updated = True
        
        for row in self.rows:
            updated = self.find_possibilities(row, 'row') or updated
        
        for col in self.cols:
            updated = self.find_possibilities(col, 'col') or updated
        
        for group in self.groups:
            updated = self.find_possibilities(group, 'group') or updated
        
        return updated

    @staticmethod
    def find_possibilities(coll, entity_type: str):
        updated = False
        indices = {}
        for ii in range(1, 10):
            for cell in coll.cells:
                if ii in cell.options:
                    if ii not in indices:
                        indices[ii] = []
                    indices[ii].append(cell)
        for key, value in indices.items():
            if len(value) == 1:
                value[0].set_value(key, f'only possibility in {entity_type}')
                updated = True
        return updated

    def group_str(self, start, end):
        return '\n'.join([str(x) for x in self.rows[start:end]])

    def __str__(self):
        header = '_' * 19
        footer = '-' * 19
        g1 = self.group_str(0, 3)
        g2 = self.group_str(3, 6)
        g3 = self.group_str(6, 9)
        sep = '-' * 19
        return f'{header}\n{g1}\n{sep}\n{g2}\n{sep}\n{g3}\n{footer}'


def import_csv(filename: str):
    data = []
    with open(f'{filename}.csv', 'rt') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            for ss in row:
                if ss == '':
                    ss = '0'
                data.append(int(ss))
        return data


if __name__ == '__main__':
    # Create the grid
    csv_data = import_csv('167')
    g = Grid(csv_data)
    print(g)
    while g.solve():
        print(g)
