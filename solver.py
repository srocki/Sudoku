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

    def set_value(self, value: int, reason: str):
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
        # TODO: RCP: Extract these and inplement the rules from: https://sudoku.com/sudoku-rules
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

        # X-Wing
        updated = self.process_x_wings() or updated

        return updated

    @staticmethod
    def find_x_wings(rows):
        res = []

        # Iterate the rows and find the indices of each number in the options
        rowdata = {}
        for ii_row in range(9):
            rowdata[ii_row] = {}
            for num in range(1, 10):
                rowdata[ii_row][num] = []
                for ii_cells in range(9):
                    if num in rows[ii_row].cells[ii_cells].options:
                        rowdata[ii_row][num].append(ii_cells)
                # remove all rowdata entries that are not 2 elements long
                rowdata[ii_row] = {k: v for k, v in rowdata[ii_row].items() if len(v) == 2}

        for num in range(1, 10):
            numdata = {}
            for ii_row in range(9):
                if num in rowdata[ii_row]:
                    numdata[ii_row] = rowdata[ii_row][num]
            if len(numdata) == 2:
                value_list = list(numdata.values())
                if value_list[0] == value_list[1]:
                    print(f"Found X-wing for number [{num}] in rows {list(numdata.keys())} and cols {value_list[0]}")
                    res.append((num, list(numdata.keys()), value_list[0]))
        return res

    def process_x_wings(self) -> bool:
        x_wings = Grid.find_x_wings(self.rows)
        updated = False
        for x_wing in x_wings:
            num = x_wing[0]
            rows = x_wing[1]
            cols = x_wing[2]
            for ii_col in cols:
                col = self.cols[ii_col]
                for ii_row in range(9):
                    if ii_row not in rows:
                        if num in col.cells[ii_row].options:
                            col.cells[ii_row].remove_option(num)
                            updated = True
        return updated

    @staticmethod
    def find_possibilities(coll, entity_type: str):
        updated = False

        # Find where the is only one place for a number with the given collection
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

        # Find where we have pairs (or triples, etc) in the collection that must contain all of the numbers in the pair (or triple...)
        def make_key(options):
            return ','.join([str(x) for x in options])

        groups = {}
        for cell in coll.cells:
            if len(cell.options) > 1:
                if make_key(cell.options) not in groups:
                    groups[make_key(cell.options)] = 0
                groups[make_key(cell.options)] = groups[make_key(cell.options)] + 1
        for key, value in groups.items():
            keys = [int(x) for x in key.split(',')]
            if len(keys) == value:
                # we have items we can remove from elements in the collection
                for cell in coll.cells:
                    if len(cell.options) > 1:
                        if not cell.options == keys:
                            for val in keys:
                                if val in cell.options:
                                    cell.remove_option(val)
                                    updated = True

        return updated

    def cells_str(self, str_lengths, row, start, end):
        row_strings = []
        for jj in range(start, end):
            cell_str = self.pad_cell_text(row.cells[jj], str_lengths[jj])
            row_strings.append(cell_str)
        return ','.join(row_strings)

    def row_str(self, str_lengths, row):
        g1 = self.cells_str(str_lengths, row, 0, 3)
        g2 = self.cells_str(str_lengths, row, 3, 6)
        g3 = self.cells_str(str_lengths, row, 6, 9)
        return f'|{g1}|{g2}|{g3}|'

    def group_str(self, str_lengths, start, end):
        return '\n'.join([self.row_str(str_lengths, x) for x in self.rows[start:end]])

    @staticmethod
    def pad_cell_text(cell, length):
        cell_str = str(cell)
        blank_str = ' ' * length
        full_str = blank_str + cell_str
        return full_str[-length:]

    def __str__(self):
        str_lengths = [max([len(str(row.cells[ii])) for row in self.rows]) for ii in range(9)]

        header = '_' * (sum(str_lengths) + 10)
        sep = '-' * (sum(str_lengths) + 10)
        g1 = self.group_str(str_lengths, 0, 3)
        g2 = self.group_str(str_lengths, 3, 6)
        g3 = self.group_str(str_lengths, 6, 9)
        return f'{header}\n{g1}\n{sep}\n{g2}\n{sep}\n{g3}\n{sep}'


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
