import sys
import cross_set

# Script must be run directly, not imported
if __name__ == '__main__':

    # Script requires one argument: filename
    if len(sys.argv) < 2:
        print("Filename argument required")
        sys.exit(1)

    # Filename is the first argument (sys.argv[0] is the program name)
    filename = sys.argv[1]

    # Read from the provided filename, assuming it exists
    puzzle_contents = ""
    with open(filename) as puzzle_file:
        puzzle_contents = puzzle_file.read()

    # Stuff the contents into puzzle (list of list of sets) with minimal validation
    puzzle = []
    # Each line: Add a list to puzzle
    for line in puzzle_contents.strip().split('\n'):
        puzzle_line = []
        # Each cell: Add a set to puzzle_line
        for cell in line.split(' '):
            # Discard spaces used for alignment
            if cell == '':
                continue
            # Each number: Convert to an int before adding to the set
            cell_numbers = (int(x) for x in cell)
            puzzle_line.append(set(cell_numbers))
        puzzle.append(puzzle_line)

    puzzle_grid = cross_set.PuzzleGrid(puzzle)

    solved_grid = cross_set.solve(puzzle_grid)
    print(solved_grid)
