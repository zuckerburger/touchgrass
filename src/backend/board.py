from dataclasses import dataclass
from typing import Optional, Tuple

from .zobrist import (
    hash_board,
    hash_piece,
    hash_move,
    hash_en_passant,
    hash_castle,
    hash_promotion,
    hash_turn,
)
from .zobrist import WKING_LONG, WKING_SHORT, BKING_LONG, BKING_SHORT, DEFAULT_CASTLING



@dataclass
class MoveRecord:
    moved_piece: int
    captured_piece: int
    promotion: Optional[int] = None
    from_sq: Tuple[int, int] = (0, 0)
    to_sq: Tuple[int, int] = (0, 0)
    en_passant: bool = False
    castling_rights: int = DEFAULT_CASTLING
    en_passant_file: Optional[int] = None


EMPTY = 0
WPAWN, WKNIGHT, WBISHOP, WROOK, WQUEEN, WKING = 1, 2, 3, 4, 5, 6
BPAWN, BKNIGHT, BBISHOP, BROOK, BQUEEN, BKING = -1, -2, -3, -4, -5, -6

class Board:
    def __init__(self):
        self.board = self.starting_pos()
        self.wking_pos = (7, 4)
        self.bking_pos = (0, 4)
        self.castling_rights = DEFAULT_CASTLING
        self.en_passant_file = None
        self.hash = hash_board(self.board)

    def starting_pos(self):
        return [
            [BROOK, BKNIGHT, BBISHOP, BQUEEN, BKING, BBISHOP, BKNIGHT, BROOK],
            [BPAWN, BPAWN, BPAWN, BPAWN, BPAWN, BPAWN, BPAWN, BPAWN],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
            [WPAWN, WPAWN, WPAWN, WPAWN, WPAWN, WPAWN, WPAWN, WPAWN],
            [WROOK, WKNIGHT, WBISHOP, WQUEEN, WKING, WBISHOP, WKNIGHT, WROOK],
        ]

    def apply_move(self, move):
        (fx, fy), (tx, ty) = move
        # CAPTURED PIECE POSITION
        (cx, cy) = (tx, ty)

        original_piece = self.board[fx][fy]
        captured = self.board[tx][ty]

        self.board[tx][ty] = original_piece
        self.board[fx][fy] = EMPTY
        en_passant = False

        removed_castle_right = 0
        old_castling_rights = self.castling_rights
        old_en_passant_file = self.en_passant_file
        self.en_passant_file = None

        if original_piece == WKING:
            self.wking_pos = (tx, ty)
            removed_castle_right = WKING_LONG | WKING_SHORT
        elif original_piece == BKING:
            self.bking_pos = (tx, ty)
            removed_castle_right = BKING_LONG | BKING_SHORT
        elif original_piece == WROOK and fx == 7:
            removed_castle_right = WKING_LONG if fy == 0 else WKING_SHORT
        elif original_piece == BROOK and fx == 0:
            removed_castle_right = BKING_LONG if fy == 0 else BKING_SHORT

        # CHECK IF PSEUDO-LEGAL EN PASSANT CAPTURE EXISTS FOR NEXT TURN
        elif abs(original_piece) == WPAWN and abs(tx - fx) == 2:
            if (
                (ty <= 6 and self.board[tx][ty + 1] == -original_piece)
                or (ty >= 1 and self.board[tx][ty - 1] == -original_piece)
            ):
                self.en_passant_file = fy

        # HANDLE EN PASSANT
        elif captured == EMPTY and abs(original_piece) == WPAWN:
            if fy != ty:
                cx = tx + abs(original_piece)
                captured = self.board[cx][cy]
                self.board[cx][cy] = EMPTY
                en_passant = True

        # HANDLE CASTLING
        # CHECK IF KING MADE A 2SQR MOVE
        if abs(original_piece) == WKING and abs(fy - ty) == 2:
            # SHORT
            if ty == 6:
                cy = 7
                rook = self.board[fx][cy]
                self.board[fx][5] = rook  # move rook
                self.board[fx][7] = EMPTY  # empty the sqr
                self.hash = hash_piece(self.hash, rook, (fx, 5))
            # LONG
            elif ty == 2:
                cy = 0
                rook = self.board[fx][cy]
                self.board[fx][3] = rook  # move rook
                self.board[fx][cy] = EMPTY
                self.hash = hash_piece(self.hash, rook, (fx, 3))

        promotion = None
        if original_piece == WPAWN and tx == 0:
            promotion = WQUEEN
            self.board[tx][ty] = WQUEEN
        elif original_piece == BPAWN and tx == 7:
            promotion = BQUEEN
            self.board[tx][ty] = BQUEEN

        self.castling_rights &= ~(removed_castle_right)
        self.update_hashes(
            original_piece,
            move,
            captured,
            (cx, cy),
            old_castling_rights,
            old_en_passant_file,
            promotion
        )

        return MoveRecord(
            moved_piece=original_piece,
            captured_piece=captured,
            promotion=promotion,
            from_sq=(fx, fy),
            to_sq=(tx, ty),
            en_passant=en_passant,
            castling_rights=old_castling_rights,
            en_passant_file=old_en_passant_file,
        )

    def undo_move(self, move, move_record):
        (fx, fy), (tx, ty) = move
        (cx, cy) = (tx, ty)
        # piece = self.board[tx][ty]

        self.board[fx][fy] = move_record.moved_piece
        self.board[tx][ty] = move_record.captured_piece

        old_castling_rights = self.castling_rights
        old_en_passant_file = self.en_passant_file

        self.castling_rights = move_record.castling_rights
        self.en_passant_file = move_record.en_passant_file

        if move_record.moved_piece == WKING:
            self.wking_pos = (fx, fy)
        elif move_record.moved_piece == BKING:
            self.bking_pos = (fx, fy)
        # CASTLING UNDO
        if abs(move_record.moved_piece) == WKING and abs(fy - ty) == 2:
            # SHORT
            if ty == 6:
                cy = 5
                rook = self.board[fx][cy]
                self.board[fx][7] = rook  # undo rook
                self.board[fx][cy] = EMPTY
                self.hash = hash_piece(self.hash, rook, (fx, 7))

            # LONG
            elif ty == 2:
                cy = 3
                rook = self.board[fx][cy]
                self.board[fx][0] = rook  # undo rook
                self.board[fx][cy] = EMPTY
                self.hash = hash_piece(self.hash, rook, (fx, 0))

        # ENPASSANT UNDO
        elif move_record.en_passant:
            self.board[tx][ty] = EMPTY
            cx = tx + abs(move_record.moved_piece)
            self.board[cx][ty] = move_record.captured_piece

        # RESTORE HASHES
        self.update_hashes(
            move_record.moved_piece,
            (move_record.from_sq, move_record.to_sq),
            move_record.captured_piece,
            (cx, cy),
            old_castling_rights,
            old_en_passant_file,
            move_record.promotion
        )

    def update_hashes(
        self,
        moved_piece,
        move,
        captured_piece,
        captured_position,
        old_castling_rights,
        old_en_passant_file,
        promotion
    ):
        self.hash = hash_move(self.hash, moved_piece, move)
        self.hash = hash_piece(self.hash, captured_piece, captured_position)
        self.hash = hash_castle(self.hash, old_castling_rights, self.castling_rights)
        self.hash = hash_en_passant(self.hash, old_en_passant_file)
        self.hash = hash_en_passant(self.hash, self.en_passant_file)
        self.hash = hash_promotion(self.hash, moved_piece, move[1], promotion)
        self.hash = hash_turn(self.hash)
