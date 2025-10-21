import random

from typing import Tuple, List

NUM_SQUARES = 64
NUM_PIECES = 12


class ZobristHasher:
    zobrist_table = {
        "pieces": [
            [random.getrandbits(64) for _ in range(NUM_SQUARES)]
            for _ in range(NUM_PIECES)
        ],
        "turn": random.getrandbits(64),
        "en-passant": [random.getrandbits(64) for _ in range(8)],
        "castling": [random.getrandbits(64) for _ in range(4)],
    }

    def hash_board(self, board: List[List[int]]):
        hash = 0
        for i in range(8):
            for j in range(8):
                hash = self.hash_piece(hash, board[i][j], (i, j))

        hash = self.hash_castle(hash, True, True)
        hash = self.hash_castle(hash, True, False)
        hash = self.hash_castle(hash, False, True)
        hash = self.hash_castle(hash, False, False)

    def hash_turn(self, hash):
        return hash ^ self.zobrist_table["turn"]

    def hash_piece(self, hash: int, piece: int, position: Tuple[int, int]):
        piece = piece - 1 if piece > 0 else piece
        piece += 6
        fx, fy = position
        randomNum = self.zobrist_table["pieces"][piece][fx * 8 + fy]
        return hash ^ randomNum

    def hash_castle(self, hash: int, isWhite: bool, isLong: bool):
        return hash ^ self.zobrist_table["castling"][isWhite * 2 + isLong]

    def hash_en_passant(self, hash: int, rank: int):
        return hash ^ self.zobrist_table["en-passant"][rank]
