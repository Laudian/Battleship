from enum import Enum


class Orientation(Enum):
    VERTICAL = 1
    HORIZONTAL = 2


class BSBoardResult(Enum):
    OUT_OF_BOUNDS = 0
    REPEAT_SHOT = 1
    MISS = 2
    HIT = 3
    HIT_AND_SUNK = 4
    END = 5


class BSBoardState(Enum):
    OUT_OF_BOUNDS = 0
    SHIP = 1
    WATER = 2
    HIT = 3
    MISS = 4
    SUNK = 5


class Ship(object):
    def __init__(self, x: int, y: int, orientation: "Orientation", size: int):
        self.size = size
        self.board: "BattleshipBoard" = None
        delta_x = 1 if orientation == Orientation.HORIZONTAL else 0
        delta_y = not delta_x

        self.squares = []
        for n in range(size):
            pos = (x, y)
            self.squares.append(pos)
            x += delta_x
            y += delta_y

    def register(self, board: "BattleshipBoard"):
        self.board = board
        for square in self.squares:
            board.board[square] = self

    def hit(self, square):
        self.size -= 1
        if self.size == 0:
            for square in self.squares:
                self.board.board[square] = BSBoardState.SUNK
            self.board.ships.remove(self)
            return BSBoardResult.HIT_AND_SUNK
        else:
            self.board.board[square] = BSBoardState.HIT
            return BSBoardResult.HIT


class BattleshipBoard(object):
    def __init__(self, ships, size):
        self.size = size
        self.board = dict()
        self.ships = ships

        for x in range(1, size+1):
            for y in range(1, size + 1):
                self.board[(x, y)] = BSBoardState.WATER

        for ship in ships:
            ship.register(self)
        return

    def mark(self, square, marker):
        self.board[square] = marker

    def move(self, square):
        current = self.board.get(square, BSBoardState.OUT_OF_BOUNDS)
        if current == BSBoardState.OUT_OF_BOUNDS:
            return BSBoardResult.OUT_OF_BOUNDS
        elif current in (BSBoardState.HIT, BSBoardState.MISS, BSBoardState.SUNK):
            return BSBoardResult.REPEAT_SHOT
        elif current == BSBoardState.WATER:
            self.board[square] = BSBoardState.MISS
            return BSBoardResult.MISS
        elif isinstance(current, Ship):
            result = current.hit(square)
            if result == BSBoardResult.HIT:
                return result
            elif result == BSBoardResult.HIT_AND_SUNK:
                if self.ships:
                    return result
                else:
                    return BSBoardResult.END
