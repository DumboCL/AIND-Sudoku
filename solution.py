import re

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(A, B):
    return [s+t for s in A for t in B]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
BOARD_SIZE = len(row_units)
diagonal1 = [['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9']]
diagonal2 = [['A9', 'B8', 'C7', 'D6', 'E5', 'F4', 'G3', 'H2', 'I1']]
unitlist = row_units + column_units + square_units + diagonal1 + diagonal2
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

####
# for Pygame

assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

# for Pygame end
#####

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Find all instances of naked twins
    all_two_digits_boxes = [box for box in values.keys() if len(values[box]) == 2]
    for box in all_two_digits_boxes:
        for unit in units[box]:
            if len([position for position in unit if values[position] == values[box]]) == 2:
                # Eliminate the naked twins as possibilities for their peers
                for item in unit:
                    if values[item] != values[box]:
                        values[item] = values[item].replace(values[box][0], '')
                        values[item] = values[item].replace(values[box][1], '')
    return values

def grid_values(grid):
    """Convert grid string into {<box>: <value>} dict with '123456789' value for empties.

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '123456789' if it is empty.
    """
    assert re.match( r'^[1-9.]{81}$', grid, re.M|re.I), "Input grid must be a string of length 81 (9x9), and only contain digits 1-9 and ."
    initial_grid = dict(zip(boxes,grid))
    for k,v in initial_grid.items():
        if v == '.':
            initial_grid[k] = '123456789'      
    return initial_grid

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print

def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    for k, v in values.items():
        if re.match(r'^\d{1}$', v):
            for position in peers[k]:
                values[position] = values[position].replace(v, '')
    return values

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    for unit in unitlist:
        for each_digit in '123456789':
            hits = 0
            target_box = ''
            for box in unit:
                if each_digit in values[box]:
                    hits += 1
                    target_box = box
                if hits > 1:
                    break
            if hits == 1:
                values[target_box] = each_digit
    return values

def reduce_puzzle(values):
    """Using three strategy to reduce every box's possible values.
    
    Three strategy:
        Eliminate
        Only Choice
        Naked Twins
        
    Input: Sudoku in dictionary form.
    Output: Resulting in dictionary form after three strategy
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Eliminate
        values = eliminate(values)

        # Only Choice
        values = only_choice(values)
        
        # Naked Twins
        values = naked_twins(values)
        
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def is_diagonal_sudoku(values):
    """Determine a Sudoku result is a Diagonal Sudoku or not.
    
    Input: Sudoku in dictionary form.
    Output: True if Diagonal Sudoku
            False if not
    """
    check_pass = False
    board = row_units
    BOARD_SIZE = len(board)

    diagonal1 = [board[i][i] for i in range(BOARD_SIZE)]
    diagonal2 = [board[i][BOARD_SIZE-1-i] for i in range(BOARD_SIZE)]
    
    if is_unit_solved(values, diagonal1) and is_unit_solved(values, diagonal2):        
        return True
    else:
        return False
    
def is_unit_solved(values, unit):
    """Determine if one unit has been solved.
    
    Input: Sudoku in dictionary form;
           Boxes set of one unit.
    Output: True if the unit solved
            False if not
    """
    print(unit)
    display(values)
    if all(len(values[s]) == 1 for s in unit):
        contrast_string = '123456789'
        for each_box in unit:
            if values[each_box] in contrast_string:
                contrast_string = contrast_string.replace(values[each_box], '')
            else:
                return False
        return True
    else:
        return False

def search(values):
    """After trying all the strategy, the last step is enumerate all the possibilities in one box, then use recursion to solve each.
    
    Input: Sudoku in dictionary form.
    Output: Solved Sudoku if found
            False if not
    """
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values
    # Choose one of the unfilled squares with the fewest possibilities
    unsolved_boxes = [box for box in boxes if len(values[box]) > 1]
        
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    candidate_no, position = min((len(values[s]),s) for s in unsolved_boxes)
    for value in values[position]:
        assumed_solution = values.copy()
        assumed_solution[position] = value
        attempt = search(assumed_solution)
        if attempt:
            return attempt
            # change this solution to : add diagonal units into original unitlist, join the solving strategy at first place
            # if is_diagonal_sudoku(attempt):
            #    return attempt
            # else:
            #    continue

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search((grid_values(grid)))

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))
'''
    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
'''