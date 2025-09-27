from .board import Board
import random
from .move_gen import getLegalMoves, isSquareAttacked


class Game:
    def __init__(self):
        self.board = Board()
        self.turn = "white"

        self.game_over = False
        self.result = None

    def is_check(self, color):
        king_pos = self.board.wking_pos if color == "white" else self.board.bking_pos
        return isSquareAttacked(self.board, *king_pos, by_white=(color == "black"))

    def get_gamestate(self):
        moves = self.legal_moves()

        if moves:
            return "ongoing"

        if self.is_check(self.turn):
            winner = "white" if self.turn == "black" else "black"
            return f"checkmate_{winner}"
        else:
            return "stalemate"

    def legal_moves(self):
        return getLegalMoves(self.board, self.turn)

    def make_move(self, move):
        if move not in self.legal_moves():
            print("> illegal move\n")
            return None

        captured = self.board.apply_move(move)

        self.turn = "black" if self.turn == "white" else "white"

        state = self.get_gamestate()
        if state != "ongoing":
            self.game_over = True
            self.result = state

        return captured

    def play_random(self):
        moves = self.legal_moves()

        if not moves:
            return None

        move = random.choice(moves)

        self.make_move(move)
        return move
