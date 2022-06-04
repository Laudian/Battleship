from battleshipboard import *

ships = [Ship(1, 1, Orientation.HORIZONTAL, 2),
         Ship(3, 3, Orientation.VERTICAL, 3)]
board = BattleshipBoard(ships, 10)


def move(x, y):
    result = board.move((x, y))
    print(result)


move(0, 0)
move(1, 1)
move(1, 2)
move(2, 1)
move(3, 3)
move(3, 4)
move(3, 5)


class BattleshipGame(object):
    def __init__(self, size, ships1, ships2):
        player1_board = BattleshipBoard(ships1, size)
        player2_board = BattleshipBoard(ships2, size)
        player1_history = BattleshipBoard([], size)
        player2_history = BattleshipBoard([], size)
