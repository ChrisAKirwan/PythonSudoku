from tkinter import *

DEFAULT_BOARD = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],

    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],

    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]
CUSTOM_BOARD = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],

    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],

    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]
TEST_BOARD = [
    [5, 3, 4, 6, 7, 8, 9, 1, 2],
    [6, 7, 2, 1, 9, 5, 3, 4, 8],
    [1, 9, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 7, 6, 1, 4, 2, 3],
    [4, 2, 6, 8, 5, 3, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 5, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 9, 0]
]

BOARDS = [DEFAULT_BOARD, CUSTOM_BOARD]  # Available boards
MARGIN = 20  # Pixels around the board
SIDE = 50  # Width of every board cell
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9


class SudokuGame:
    def __init__(self):
        self.start_puzzle = []
        self.puzzle = []
        self.solved_puzzle = []
        self.game_over = False

    def check_win(self):
        # Check same row
        find = self.__find_empty()
        if not find:
            return True
        return False

    @staticmethod
    def is_valid_value(pos, value, board):

        if value == 0:
            return True

        row = pos[0]
        col = pos[1]

        # Check same row
        for i in range(len(board[row])):
            if board[row][i] == value and i != col:
                return False

        # Check each row with same element pos
        for i in range(len(board)):
            if board[i][col] == value and i != row:
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
                if board[i][j] == value:
                    return False

        return True

    def __find_empty(self, board=None):
        if board is None:
            board = self.puzzle

        for row in range(len(board)):
            for element in range(len(board[row])):
                if board[row][element] == 0:
                    return row, element

    def solve_board(self, solved_puzzle=None):
        if solved_puzzle is None:
            solved_puzzle = SudokuGame.copy_puzzle(self.puzzle)
        # While there are still empty spaces,
        # find the next empty space.
        # find a valid number that fits.
        # find the next empty space.
        # if no valid numbers, return to previous space and increment.
        # repeat until end of board.
        # if no valid value in first space, board is unsolvable.

        # ----

        # check if there's an empty space
        # if so, assign the position to a variable.
        # iterate through 1-9 and find a valid number.
        # recursively call solve_board
        # if there are no valid numbers, return, continue through the previous loop.

        find = self.__find_empty(solved_puzzle)
        if not find:
            return solved_puzzle  # Puzzle has been solved.
        else:
            row, col = self.__find_empty(solved_puzzle)

        for i in range(1, 10):
            if SudokuGame.is_valid_value([row, col], i, solved_puzzle):
                solved_puzzle[row][col] = i

                if self.solve_board(solved_puzzle):
                    return solved_puzzle

                solved_puzzle[row][col] = 0

        return None

    def check_valid(self, pos, value):
        if value == self.solved_puzzle[pos[0]][pos[1]]:
            return True
        return False

    @staticmethod
    def copy_puzzle(puzzle_a):
        puzzle_b = []
        for i in range(9):
            puzzle_b.append([])
            for j in range(9):
                puzzle_b[i].append(puzzle_a[i][j])

        return puzzle_b


class MainUIFlow(Frame):
    def __init__(self, parent, game):
        self.game = game
        self.parent = parent
        self.row, self.col = -1, -1
        self.is_custom = False
        Frame.__init__(self, parent)

        self._gametype_page = GameTypeSelectionPage(self)  # Show Normal, Custom buttons
        self._defaultgame_page = DefaultGamePage(self)  # Show New Game, Clear Answers, Solve Puzzle buttons
        self._customgame_page = CustomGamePage(self)    # Show New Game, Confirm buttons
        self._victory_page = VictoryPage(self)          # Show New Game, Show Board buttons

        _buttonframe = Frame(self)
        _container = Frame(self)

        _buttonframe.pack(side="top", fill="x", expand=False)
        _container.pack(side="top", fill="both", expand=True)

        self._gametype_page.place(in_=_container, x=0, y=0, relwidth=1, relheight=1)
        self._defaultgame_page.place(in_=_container, x=0, y=0, relwidth=1, relheight=1)
        self._customgame_page.place(in_=_container, x=0, y=0, relwidth=1, relheight=1)
        self._victory_page.place(in_=_container, x=0, y=0, relwidth=1, relheight=1)

        self.__init_buttons(_buttonframe)
        self._select_game_type()

    def __init_buttons(self, button_frame):
        self._gametype_button = Button(button_frame, text="New Game", command=self._select_game_type)
        self._default_button = Button(button_frame, text="Normal Game", command=self._start_default_game)
        self._custom_button = Button(button_frame, text="Custom Game", command=self._start_custom_game)
        self._clear_button = Button(button_frame, text="Clear Answers",
                                    command=self._clear_answers)
        self._victory_button = Button(button_frame, text="Show Board", command=self._show_board)
        self._confirm_button = Button(button_frame, text="Confirm Placement", command=self._confirm_placement)
        self._solve_button = Button(button_frame, text="Solve Puzzle", command=self._solve_puzzle)

        self._gametype_button.pack(side="left")
        self._default_button.pack(side="left")
        self._custom_button.pack(side="left")
        self._clear_button.pack(side="left")
        self._victory_button.pack(side="left")
        self._confirm_button.pack(side="left")
        self._solve_button.pack(side="left")

    def _clear_buttons(self):
        self._gametype_button.pack_forget()
        self._default_button.pack_forget()
        self._custom_button.pack_forget()
        self._clear_button.pack_forget()
        self._victory_button.pack_forget()
        self._confirm_button.pack_forget()
        self._solve_button.pack_forget()

    def _select_game_type(self):
        self._gametype_page.lift()
        self._clear_buttons()

        self._default_button.pack(side="left")
        self._custom_button.pack(side="left")

        self.game.__init__()

    def _start_default_game(self):
        self._defaultgame_page.lift()
        self.is_custom = False

        self._clear_buttons()
        self._gametype_button.pack(side="left")
        self._clear_button.pack(side="left")
        self._solve_button.pack(side="left")

        if not self.game.start_puzzle:
            self.game.start_puzzle = SudokuGame.copy_puzzle(DEFAULT_BOARD)
            self.game.puzzle = SudokuGame.copy_puzzle(self.game.start_puzzle)

        if self.game.check_win():
            self.__draw_victory()

        self.game.solved_puzzle = self.game.solve_board()

        if self.game.solved_puzzle is None:
            self.game.__init__()
            self._start_custom_game()

        self.__draw_grid(self._defaultgame_page.canvas)

        self._defaultgame_page.canvas.bind("<Button-1>", lambda event,
                                           arg=self._defaultgame_page.canvas: self.__cel_clicked(event, arg))
        self._defaultgame_page.canvas.bind("<Key>", lambda event,
                                           arg=self._defaultgame_page.canvas: self.__key_pressed(event, arg))

        self.__draw_puzzle(self._defaultgame_page.canvas)

    def _start_custom_game(self):
        self._customgame_page.lift()
        self.is_custom = True

        self._clear_buttons()
        self._gametype_button.pack(side="left")
        self._confirm_button.pack(side="left")

        self.game.start_puzzle = SudokuGame.copy_puzzle(CUSTOM_BOARD)
        self.game.puzzle = SudokuGame.copy_puzzle(self.game.start_puzzle)

        self.__draw_grid(self._customgame_page.canvas)

        self._customgame_page.canvas.bind("<Button-1>", lambda event,
                                          arg=self._customgame_page.canvas: self.__cel_clicked(event, arg))
        self._customgame_page.canvas.bind("<Key>", lambda event,
                                          arg=self._customgame_page.canvas: self.__key_pressed(event, arg))

        self.__draw_puzzle(self._customgame_page.canvas)

    def _clear_answers(self):
        # self.game.puzzle = self.game.start_puzzle
        self.game.puzzle = SudokuGame.copy_puzzle(self.game.start_puzzle)
        self.__draw_puzzle(self._defaultgame_page.canvas)

    def _confirm_placement(self):
        self.game.start_puzzle = SudokuGame.copy_puzzle(self.game.puzzle)
        self._start_default_game()

    def _solve_puzzle(self):
        self.game.puzzle = SudokuGame.copy_puzzle(self.game.solved_puzzle)
        self.__draw_puzzle(self._defaultgame_page.canvas)
        self.__draw_victory()

    @staticmethod
    def __draw_grid(canvas):
        for i in range(10):
            if i % 3 == 0:
                color = "black"
            else:
                color = "gray"

            x0 = MARGIN + i * SIDE
            y0 = MARGIN
            x1 = MARGIN + i * SIDE
            y1 = HEIGHT - MARGIN
            canvas.create_line(x0, y0, x1, y1, fill=color)

            x0 = MARGIN
            y0 = MARGIN + i * SIDE
            x1 = WIDTH - MARGIN
            y1 = MARGIN + i * SIDE
            canvas.create_line(x0, y0, x1, y1, fill=color)

    def __cel_clicked(self, click_pos, canvas):
        if self.game.game_over:
            return

        x, y = click_pos.x, click_pos.y
        if (MARGIN < x < WIDTH - MARGIN and
                MARGIN < y < HEIGHT - MARGIN):
            canvas.focus_set()
            row = int((y - MARGIN) / SIDE)
            col = int((x - MARGIN) / SIDE)

            if (row, col) == (self.row, self.col):
                self.row, self.col = -1, -1
            elif self.game.puzzle[row][col] == 0:
                self.row = row
                self.col = col

        self.__draw_cursor(canvas)

    def __draw_cursor(self, canvas, color="blue"):
        canvas.delete("cursor")
        if self.row >= 0 and self.col >= 0:
            x0 = MARGIN + self.col * SIDE + 1
            y0 = MARGIN + self.row * SIDE + 1
            x1 = MARGIN + (self.col + 1) * SIDE - 1
            y1 = MARGIN + (self.row + 1) * SIDE - 1
            canvas.create_rectangle(x0, y0, x1, y1, outline=color, tags="cursor")

    def __key_pressed(self, key_val, canvas):
        if self.game.game_over:
            return

        try:
            key_input = int(key_val.char)
        except ValueError:
            self.__draw_puzzle(canvas)
            self.__draw_cursor(canvas, "red")
            return

        if self.row >= 0 and self.col >= 0 and str(key_input) in "123456789":

            color = "blue"
            self.game.puzzle[self.row][self.col] = key_input

            if self.is_custom:
                if not self.game.is_valid_value((self.row, self.col), key_input, self.game.puzzle):
                    self.game.puzzle[self.row][self.col] = self.game.start_puzzle[self.row][self.col]
                    color = "red"
            else:
                if self.game.check_valid((self.row, self.col), key_input):
                    if self.game.check_win():
                        self.__draw_victory()
                else:
                    self.game.puzzle[self.row][self.col] = self.game.start_puzzle[self.row][self.col]
                    color = "red"
                    # INCORRECT PLACEMENT..

            self.__draw_puzzle(canvas)
            self.__draw_cursor(canvas, color)

            if color == "blue":
                self.row = -1
                self.col = -1

    def _show_board(self):
        self._defaultgame_page.lift()
        self._victory_button.pack_forget()

    def __draw_victory(self):
        self._solve_button.pack_forget()
        self._clear_button.pack_forget()
        self._victory_button.pack(side="left")

        self._victory_page.lift()
        self.game.game_over = True

    def __draw_puzzle(self, canvas):
        canvas.delete("numbers")

        for i in range(9):
            for j in range(9):
                answer = self.game.puzzle[i][j]
                if answer != 0:
                    x = MARGIN + j * SIDE + SIDE / 2
                    y = MARGIN + i * SIDE + SIDE / 2
                    original = self.game.start_puzzle[i][j]

                    if answer == original:
                        color = "black"
                    else:
                        color = "green"
                    canvas.create_text(x, y, text=answer, tags="numbers", fill=color)


class Page(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)


class GameTypeSelectionPage(Page):
    def __init__(self, parent):
        Page.__init__(self, parent)
        label = Label(self, text="Choose a game type")
        label.pack(side="top", fill="both", expand=True)

        parent.game.__init__()


class DefaultGamePage(Page):
    def __init__(self, parent):
        Page.__init__(self, parent)
        label = Label(self, text="Sudoku - Normal Game")
        label.pack(side="top", fill="both", expand=True)

        self.pack(fill=BOTH, expand=True)
        self.canvas = Canvas(self, width=WIDTH, height=HEIGHT)
        self.canvas.pack(fill=BOTH, side=TOP)


class CustomGamePage(Page):
    def __init__(self, parent):
        Page.__init__(self, parent)
        label = Label(self, text="Sudoku - Custom Game")
        label.pack(side="top", fill="both", expand=True)

        self.pack(fill=BOTH, expand=True)
        self.canvas = Canvas(self, width=WIDTH, height=HEIGHT)
        self.canvas.pack(fill=BOTH, side=TOP)


class VictoryPage(Page):
    def __init__(self, parent):
        Page.__init__(self, parent)
        label = Label(self, text="Sudoku - Victory!")
        label.pack(side="top", fill="both", expand=True)

        x0 = MARGIN + SIDE * 2
        y0 = MARGIN + SIDE * 2
        x1 = MARGIN + SIDE * 7
        y1 = MARGIN + SIDE * 7

        canvas = Canvas(self, width=WIDTH, height=HEIGHT)
        canvas.create_oval(x0, y0, x1, y1, tags="victory", fill="dark orange", outline="orange")

        x = MARGIN + 4 * SIDE + SIDE / 2
        y = MARGIN + 4 * SIDE + SIDE / 2
        canvas.create_text(x, y, text="You Win!", tags="winner", fill="white", font=("Arial", 32))
        canvas.pack(fill=BOTH, side=TOP)
