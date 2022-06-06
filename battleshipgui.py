from battleshipgame import BattleshipGame, BSBoardState, Ship, Orientation
import tkinter as tk
from tkinter import font


class BSGUI(tk.Tk):
    def __init__(self, game, master=None):
        super(BSGUI, self).__init__()
        self.size = tk.IntVar(value=10)
        self.game: BattleshipGame = game
        self.currentframe = self.create_sizeframe()
        self.resizable(False, False)

    def confirm_size(self):
        self.currentframe.destroy()
        self.size: int = self.size.get()
        self.create_boardframe(0)

    def create_sizeframe(self):
        sizeframe = tk.Frame(self)
        sizeframe.pack()
        prompt = tk.Label(sizeframe, text="Wie hoch/breit soll das Spielfeld sein?")
        prompt.grid(row=0, column=0)

        sizeentry = tk.Entry(sizeframe, borderwidth=1, textvariable=self.size)
        sizeentry.grid(row=1, column=0)

        confirm = tk.Button(sizeframe, text="Ok", command=self.confirm_size)
        confirm.grid(row=1, column=1)
        return sizeframe

    def create_square(self, state, frame, command, enemy=False):
        text = ""
        if isinstance(state, Ship):
            color = "blue" if enemy else "grey"
        elif state == BSBoardState.WATER:
            color = "blue"
        elif state == BSBoardState.MISS:
            color = "blue"
            text = "MISS"

        square = tk.Button(width=6, height=3, bg=color, master=frame, text=text, command=command,
                           font=font.Font(family="Helvetica", size=10, weight=font.BOLD))
        return square

    def square_button(self, x, y):
        print((x, y))

    def create_boardframe(self, boardindex, enemy=False):
        boardframe = tk.Frame(self)
        boardframe.pack()
        for x in range(self.size):
            for y in range(self.size):
                state = self.game.boards[boardindex].grid.get((x, y), BSBoardState.OUT_OF_BOUNDS)
                square = self.create_square(state, boardframe,
                                            lambda value=(x,y): self.square_button(*value), enemy=enemy)
                square.grid(column=x, row=y)
        self.currentframe = boardframe



if __name__ == "__main__":
    ships0 = [Ship(1, 1, Orientation.HORIZONTAL, 2),
              Ship(3, 3, Orientation.VERTICAL, 3)]

    ships1 = [Ship(1, 1, Orientation.HORIZONTAL, 3),
              Ship(3, 3, Orientation.VERTICAL, 2)]

    game = BattleshipGame(12, ships0, ships1, rule_move_until_miss=True)
    game.move(0, 0)
    game.move(0, 0)

    gui: BSGUI = BSGUI(game)
    gui.mainloop()
