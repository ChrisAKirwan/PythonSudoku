from sudoku_builder import SudokuGame, MainUIFlow, WIDTH, HEIGHT
from tkinter import Tk


player_game = SudokuGame()
root = Tk()
main = MainUIFlow(root, player_game)
main.pack(side="top", fill="both", expand=True)
root.geometry("%dx%d" % (WIDTH, HEIGHT + 40))
root.mainloop()