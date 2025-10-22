import random

from typing import Tuple, List

from backend.board import DEFAULT_CASTLING, EMPTY, WKING_LONG

NUM_SQUARES = 64
NUM_PIECES = 12


zobrist_table = {
    "pieces": [
        [random.getrandbits(64) for _ in range(NUM_SQUARES)]
        for _ in range(NUM_PIECES)
    ],
    "turn": random.getrandbits(64),
    "en-passant": [random.getrandbits(64) for _ in range(8)],
    "castling": [random.getrandbits(64) for _ in range(4)],
}

def hash_board(board: List[List[int]]):
    hash = 0
    for i in range(8):
        for j in range(8):
            hash = hash_piece(hash, board[i][j], (i, j))
    hash = hash_castle(hash, 0, DEFAULT_CASTLING) 
    return hash

def hash_turn(hash):
    return hash ^ zobrist_table["turn"]

def hash_piece(hash: int, piece: int, position: Tuple[int, int]):
    if piece == EMPTY:
        return hash
    piece = piece + 5 if piece > 0 else piece + 6
    fx, fy = position
    randomNum = zobrist_table["pieces"][piece][fx * 8 + fy]
    return hash ^ randomNum

def hash_move(hash: int, piece: int, move: Tuple[Tuple[int, int], Tuple[int, int]]):
    position1, position2 = move
    return hash ^ hash_piece(hash, piece, position1) ^ hash_piece(hash, piece, position2)

def hash_castle(hash: int, old: int, new: int):
    changed_rights = (old ^ new)
    if changed_rights == 0:
        return hash

    for i in range(4):
        if changed_rights & (1 << i):
            hash ^= zobrist_table["castling"][i]
    return hash

def hash_en_passant(hash: int, rank: int | None):
    return hash if rank == None else hash ^ zobrist_table["en-passant"][rank]
