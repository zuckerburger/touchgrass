from backend.game import Game


class API:
    def __init__(self):
        self.g = Game()

    def get_state(self):
        return {
            "board": self.g.board.board,
            "turn": self.g.turn,
            "over": self.g.game_over,
            "result": self.g.result,
        }

    def move(self):
        return self.g.legal_moves()

    def play(self, move):
        return self.g.make_move(move)
