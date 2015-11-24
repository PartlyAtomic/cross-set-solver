import copy
import itertools

class PuzzleGrid(object):
    grid = None

    def __init__(self, puzzle):
        # Check that the provided grid is square
        num_rows = len(puzzle)
        for row in puzzle:
            if len(row) != num_rows:
                raise ValueError("Puzzle grid is not square")

        self.grid = copy.deepcopy(puzzle)

    def __str__(self):
        # Get the size of the largest set in the puzzle
        all_cells = (self.cell(x,y) for x,y in itertools.product(range(self.size()), range(self.size())))
        padding = max(len(cell) for cell in all_cells)
        rows = []
        for row in self.grid:
            cells = []
            for cell in row:
                # Print set(1,2,3) as 123, padding to the largest set in the puzzle
                format_str = "%% %ds" % padding
                compact_set = "".join(str(num) for num in cell)
                cells.append(format_str % compact_set)
            rows.append(" ".join(cells))
        return "\n".join(rows)

    def column(self, x):
        return (row[x] for row in self.grid)

    def row(self, y):
        return self.grid[y]

    def cell(self, x, y):
        return self.grid[y][x]

    def set_cell(self, x, y, val):
        self.grid[y][x] = val

    def size(self):
        return len(self.grid)

    def __eq__(self, other):
        return self.grid == other.grid

    def __ne__(self, other):
        return not (self == other)
