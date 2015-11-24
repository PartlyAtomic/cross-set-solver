import itertools
from cross_set.puzzle_grid import PuzzleGrid

def cell_solved(cell):
    return len(cell) == 1

def list_solved(cell_list):
    # All cells have one value
    num_solved = sum(1 for cell in cell_list if len(cell) == 1)
    if num_solved < len(cell_list):
        return False

    # There are no duplicate cells
    cell_set = set(list(cell)[0] for cell in cell_list)
    if len(cell_set) < len(cell_list):
        return False

    return True

column_solved = list_solved
row_solved = list_solved

def puzzle_solved(puzzle):
    for row_num in range(puzzle.size()):
        if not row_solved(list(puzzle.row(row_num))):
            return False

    for col_num in range(puzzle.size()):
        if not column_solved(list(puzzle.column(col_num))):
            return False

    return True

def sanity_check(puzzle):
    for row, column in itertools.product(range(puzzle.size()), range(puzzle.size())):
        cell = puzzle.cell(column, row)
        if len(cell) == 0:
            return False
    return True

# Remove invalidated cell values, this is the most basic thing to do to a puzzle
def weed(puzzle):
    old_puzzle = puzzle
    puzzle = PuzzleGrid(puzzle.grid)
    for row, column in itertools.product(range(puzzle.size()), range(puzzle.size())):
        cell = old_puzzle.cell(column, row)
        if cell_solved(cell):
            (locked_value,) = cell

            # Get a list of cells in the same row and column to weed
            in_row = ((c, row) for c in range(puzzle.size()) if not c == column)
            in_column = ((column, r) for r in range(puzzle.size()) if not r == row)
            cells_to_check = itertools.chain(in_row, in_column)

            # Read cells from the puzzle being modified and remove the locked value if it exists, saving off to the new puzzle
            for x,y in cells_to_check:
                other_cell = puzzle.cell(x, y)
                if locked_value in other_cell:
                    other_cell.remove(locked_value)

    return puzzle

def minimal_form(puzzle):
    weeded_puzzle = weed(puzzle)
    while weeded_puzzle != puzzle:
        puzzle, weeded_puzzle = weeded_puzzle, weed(puzzle)
    return weeded_puzzle

# TODO: Get singles from old_puzzle, update them on puzzle
def lock_singles(puzzle):
    old_puzzle = puzzle
    puzzle = minimal_form(puzzle)

    rows = (puzzle.row(row) for row in range(puzzle.size()))
    columns = (puzzle.column(column) for column in range(puzzle.size()))
    # Take advantage of the fact these are all references and discard WHAT they are
    cell_lists = itertools.chain(rows, columns)
    for cell_list in cell_lists:
        cell_list = list(cell_list)
        values = []
        for cell in cell_list:
            values.extend(list(cell))

        singles = (i for i in range(1, puzzle.size()+1) if values.count(i) == 1)
        for single in singles:
            for cell in cell_list:
                if single in cell:
                    # Don't update already locked cells
                    if len(cell) > 1:
                        cell.intersection_update({single})

                    # It's a single for a reason, don't need to check the rest of the cells once it's found
                    continue

    return puzzle

def ntuple_equals(puzzle):
    old_puzzle = puzzle
    puzzle = minimal_form(puzzle)

    rows = (puzzle.row(row) for row in range(puzzle.size()))
    columns = (puzzle.column(column) for column in range(puzzle.size()))
    # Take advantage of the fact these are all references and discard WHAT they are
    cell_lists = itertools.chain(rows, columns)
    for cell_list in cell_lists:
        cell_list = list(cell_list)
        ntuples = []
        for cell in cell_list:
            if cell_list.count(cell) == len(cell) and cell not in ntuples:
                ntuples.append(cell)

        for tuple in ntuples:
            for cell in cell_list:
                if cell != tuple:
                    # Remove any elements from the tuple from cell
                    cell.difference_update(tuple)

    return puzzle

def solve(puzzle):
    iterations = 1
    solved_puzzle = puzzle
    # Loop until there's no improvement
    while True:
        if not sanity_check(puzzle):
            raise RuntimeError("No solution possible.")
        solved_puzzle = minimal_form(puzzle)
        solved_puzzle = lock_singles(solved_puzzle)
        solved_puzzle = ntuple_equals(solved_puzzle)
        print("Iteration %d" % iterations)
        print(solved_puzzle)
        print()
        if puzzle_solved(puzzle) or puzzle == solved_puzzle:
            break
        else:
            puzzle = solved_puzzle
            iterations += 1

    print("Total iterations: %d" % iterations)
    return solved_puzzle

