from utils import *

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

def naked_twins(values):
    for unit in unitlist:
        box_list = []
        other_boxes = []
        for box in unit:
            if len(values[box]) == 2:
                box_list.append(values[box])
            else:
                other_boxes.append(box)
        if len(box_list) == 2 and box_list[0] == box_list[1]:
            for other_box in other_boxes:
                values[other_box] = values[other_box].replace(box_list[0][0], '').replace(box_list[0][1], '')
    return values


    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

def cross(A, B):
    return [a+b for a in A for b in B]

def grid_values(grid):
    dict = {}
    for idx in range(81):
        if grid[idx] == '.':
            dict[boxes[idx]] = '123456789'
        else:
            dict[boxes[idx]] = grid[idx]

    return dict

def display(values):
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            pos_boxes = [box for box in unit if digit in values[box]]
            if len(pos_boxes) == 1:
                values[pos_boxes[0]] = digit
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        values = only_choice(eliminate(values))

        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])

        stalled = solved_values_before == solved_values_after

        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    values = reduce_puzzle(values)

    if values is False:
        return False

    if all(len(values[box]) == 1 for box in boxes):
        return values

    _,box = min((len(values[box]), box) for box in boxes if len(values[box]) > 1)

    for val in values[box]:
        test_values = values.copy()
        test_values[box] = val
        result = search(test_values)
        if result:
            return result

def solve(grid):
    values = grid_values(grid)
    return search(values)

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
