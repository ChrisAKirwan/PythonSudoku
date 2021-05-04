def find_empty(gameBoard):
    for row in range(len(gameBoard)):
        for element in range(len(gameBoard[row])):
            if gameBoard[row][element] == 0:
                return row, element


def is_valid(gameBoard, pos, value):
    if value == 0:
        return True

    row = pos[0]
    col = pos[1]

    # Check same row
    for i in range(len(gameBoard[row])):
        if gameBoard[row][i] == value and i != col:
            return False

    # Check each row with same element pos
    for i in range(len(gameBoard)):
        if gameBoard[i][col] == value and i != row:
            return False

    # Check square
        # square 1: row 0-2, col 0-2
        # square 2: row 0-2, col 3-5
        # square 3: row 0-2, col 6-8
        # ...
        # square 9: row 6-8, col 6-8

    # row/col // 3 gives us the square location. Multiplying by
    #   an additional 3 gives us the starting position for that
    #   row/col's square.
    square_x = (row // 3) * 3
    square_y = (col // 3) * 3

    for i in range(square_x, square_x + 3):
        for j in range(square_y, square_y + 3):
            if i == row and j == col:
                continue
            if gameBoard[i][j] == value:
                return False

    return True


def solve_board(gameBoard):
    # While there are still empty spaces,
    # find the next empty space.
    # find a valid number that fits.
    # find the next empty space.
    # if no valid numbers, return to previous space and increment.
    # repeat until end of board.
    # if no valid value in first space, board is unsolvable.

    #----

    # check if there's an empty space
    # if so, assign the position to a variable.
    # iterate through 1-9 and find a valid number.
    # recursively call solve_board
    # if there are no valid numbers, return, continue through the previous loop.

    find = find_empty(gameBoard)
    if not find:
        return gameBoard # Puzzle has been solved.
    else:
        row, col = find_empty(gameBoard)

    for i in range(1, 10):
        if is_valid(gameBoard, [row, col], i):
            gameBoard[row][col] = i

            if solve_board(gameBoard):
                return gameBoard

            gameBoard[row][col] = 0

    return False

