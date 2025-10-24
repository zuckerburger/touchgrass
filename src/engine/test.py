import random
from ..backend.api import API
from .base import BaseEngine
from ..utils import uci_to_coords


class TestEngine(BaseEngine):
    def __init__(self, api: API):
        super().__init__(api)
        self.idx = 0
        self.moves = ["e7e5", "d8f6", "f6d8", "d8f6", "f6d8", "d8f6", "f6e7", "e7d8"]

    def get_best_move(self):
        moves = self.api.get_legal_moves()
        if moves:
            move = random.choice(moves)
            if self.idx < len(self.moves):
                newmove = uci_to_coords(self.moves[self.idx])
                if newmove in moves:
                    move = newmove
                else:
                    print(f"move {newmove} not legal, making random move")
                self.idx += 1
            else:
                print(f"Total moves exceeded, making random move")
            return move
        return None
