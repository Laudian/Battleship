from battleshipboard import *

ships0 = [Ship(1, 1, Orientation.HORIZONTAL, 2),
          Ship(3, 3, Orientation.VERTICAL, 3)]

ships1 = [Ship(1, 1, Orientation.HORIZONTAL, 3),
          Ship(3, 3, Orientation.VERTICAL, 2)]


class BattleshipGame(object):
    def __init__(self, size, ships0, ships1, rule_move_until_miss: bool = True):
        player0_board = BattleshipBoard(ships0, size)
        player1_board = BattleshipBoard(ships1, size)
        self.boards = [player0_board, player1_board]
        self.turn = 0
        self.rule_move_until_miss = rule_move_until_miss

    def move(self, x: int, y: int) -> BSMoveResult:
        if self.turn == 2:
            raise Exception("Cannot make move because game has finished already")
        result = self.boards[not self.turn].move((x, y))
        if result == BSMoveResult.MISS:
            self.turn = not self.turn
        elif result in [BSMoveResult.HIT, BSMoveResult.HIT_AND_SUNK]:
            if not self.rule_move_until_miss:
                self.turn = not self.turn
        elif result == BSMoveResult.END:
            self.turn = 2
        return result

    def getactiveplayer(self):
        # returns either the index of the active player or 2 if the game is over
        return int(self.turn)

    def displaygamestate(self):
        print("Player 0:")
        self.boards[0].display()
        print("Player 1:")
        self.boards[1].display()


if __name__ == "__main__":
    game = BattleshipGame(12, ships0, ships1, rule_move_until_miss=False)
    game.displaygamestate()
    player0moves = [(1, 1), (2, 1), (3, 1), (3, 3), (3, 4), (5, 5), (24, 24)]
    player1moves = [(1, 1), (2, 1), (3, 3), (3, 4), (3, 5), (3, 5)]
    playermoves = [player0moves, player1moves]
    result = None
    while True:
        currentplayer = game.getactiveplayer()
        if currentplayer == 2:
            print("Game has ended")
            game.displaygamestate()
            break
        else:
            move = playermoves[currentplayer].pop()
            print(f"Current Player: {currentplayer}. Move: {move}")
            game.move(*move)
