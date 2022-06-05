from enum import Enum


class Orientation(Enum):
    VERTICAL = 1
    HORIZONTAL = 2


class BSMoveResult(Enum):
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
            board.grid[square] = self

    def hit(self, square):
        self.size -= 1
        if self.size == 0:
            for square in self.squares:
                self.board.grid[square] = BSBoardState.SUNK
            self.board.ships.remove(self)
            return BSMoveResult.HIT_AND_SUNK
        else:
            self.board.grid[square] = BSBoardState.HIT
            return BSMoveResult.HIT


class BattleshipBoard(object):
    def __init__(self, ships, size):
        self.size = size
        self.grid = dict()
        self.ships = ships

        for x in range(size):
            for y in range(size):
                self.grid[(x, y)] = BSBoardState.WATER

        for ship in ships:
            ship.register(self)
        return

    def mark(self, square, marker):
        self.grid[square] = marker

    @staticmethod
    def state_to_char(state: BSBoardState) -> str:
        if state == BSBoardState.WATER:
            return " "
        elif state == BSBoardState.HIT:
            return "X"
        elif state == BSBoardState.SUNK:
            return "#"
        elif state == BSBoardState.MISS:
            return "O"
        elif isinstance(state, Ship):
            return "S"
        else:
            raise ValueError(f"State {state} has no representation.")

    def move(self, square) -> BSMoveResult:
        current = self.grid.get(square, BSBoardState.OUT_OF_BOUNDS)
        if current == BSBoardState.OUT_OF_BOUNDS:
            return BSMoveResult.OUT_OF_BOUNDS
        elif current in (BSBoardState.HIT, BSBoardState.MISS, BSBoardState.SUNK):
            return BSMoveResult.REPEAT_SHOT
        elif current == BSBoardState.WATER:
            self.grid[square] = BSBoardState.MISS
            return BSMoveResult.MISS
        elif isinstance(current, Ship):
            result = current.hit(square)
            if result == BSMoveResult.HIT:
                return result
            elif result == BSMoveResult.HIT_AND_SUNK:
                if self.ships:
                    return result
                else:
                    return BSMoveResult.END

    def display(self):
        print((2 * self.size + 1) * "_")
        for y in range(self.size):
            rowstring: str = "|"
            for x in range(self.size):
                rowstring += self.state_to_char(self.grid[(x, y)]) + "|"
            print(rowstring)
        print((2 * self.size + 1) * "_")
