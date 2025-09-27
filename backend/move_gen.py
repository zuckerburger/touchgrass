from .pieces import getPseudoLegalMoves, in_bounds
from .board import WPAWN, WKNIGHT, WBISHOP, WROOK, WQUEEN, WKING
from .board import EMPTY
from .board import BPAWN, BKNIGHT, BBISHOP, BROOK, BQUEEN, BKING


def isSquareAttacked(board, x, y, by_white):
    # pawns
    direction = -1 if by_white else 1
    for dy in [-1, 1]:
        nx, ny = x + direction, y + dy
        if in_bounds(nx, ny) and board.board[nx][ny] == (WPAWN if by_white else BPAWN):
            return True

    # knights
    for dx, dy in [
        (2, 1),
        (1, 2),
        (-1, 2),
        (-2, 1),
        (-2, -1),
        (-1, -2),
        (1, -2),
        (2, -1),
    ]:
        nx, ny = x + dx, y + dy
        if in_bounds(nx, ny) and board.board[nx][ny] == (
            WKNIGHT if by_white else BKNIGHT
        ):
            return True

    # bishops queens
    for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
        nx, ny = x + dx, y + dy
        while in_bounds(nx, ny):
            p = board.board[nx][ny]
            if p != EMPTY:
                if p == (WBISHOP if by_white else BBISHOP) or p == (
                    WQUEEN if by_white else BQUEEN
                ):
                    return True
                break
            nx += dx
            ny += dy

    # rooks queens
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        while in_bounds(nx, ny):
            p = board.board[nx][ny]
            if p != EMPTY:
                if p == (WROOK if by_white else BROOK) or p == (
                    WQUEEN if by_white else BQUEEN
                ):
                    return True
                break
            nx += dx
            ny += dy

    # king
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if in_bounds(nx, ny) and board.board[nx][ny] == (
                WKING if by_white else BKING
            ):
                return True

    return False


def getLegalMoves(board, color):
    moves = []

    for x in range(8):
        for y in range(8):
            piece = board.board[x][y]
            if piece == 0:
                continue
            if color == "white" and piece < 0:
                continue
            if color == "black" and piece > 0:
                continue

            for nx, ny in getPseudoLegalMoves(board.board, x, y):
                move = ((x, y), (nx, ny))
                captured = board.apply_move(move)

                king_pos = board.wking_pos if color == "white" else board.bking_pos
                if not isSquareAttacked(board, *king_pos, by_white=(color == "black")):
                    moves.append(move)
                board.undo_move(move, captured)

    return moves
