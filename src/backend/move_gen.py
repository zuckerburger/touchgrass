from .pieces import getPseudoLegalMoves, in_bounds
from .board import WPAWN, WKNIGHT, WBISHOP, WROOK, WQUEEN, WKING
from .board import EMPTY
from .board import BPAWN, BKNIGHT, BBISHOP, BROOK, BQUEEN, BKING


def isSquareAttacked(board, x, y, by_white):
    # pawns
    direction = 1 if by_white else -1
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



def canCastle(board, color, side, history):
    row=7 if color=="white" else 0
    king=WKING if color=="white" else BKING
    
    if side=="SHORT":
        castle_rook=WROOK if color=="white" else BROOK
        
        #CHECK LINE OF SIGHT                         || NOT CHECK ||           ROOK PRESENT AT SHORT SIDE(H1//H8)    ||     KING AT HOME
        if board.board[row][5]==0 and board.board[row][6]==0 and isSquareAttacked(board, row, 4, by_white=(color == "black"))==False and board.board[row][7]==4 and board.board[row][4]==6:
            #HISTORY CHECK
            for move in history:
                if move.moved_piece==king:
                    return False
                elif move.moved_piece==castle_rook and move.from_sq==(row,7):
                    return False
        return True
            
    
    elif side=="LONG":
        castle_rook=WROOK if color=="white" else BROOK
        
        #                  CHECK LINE OF SIGHT                              || NOT CHECK ||           ROOK PRESENT AT LONG SIDE(A1//A8)    ||     KING AT HOME
        if board.board[row][1]==0 and board.board[row][2]==0 and board.board[row][3]==0 and isSquareAttacked(board, row, 4, by_white=(color == "black"))==False and board.board[row][0]==4 and board.board[row][4]==6:
            #HISTORY CHECK
            for move in history:
                if move.moved_piece==king:
                    return False
                elif move.moved_piece==castle_rook and move.from_sq==(row,0):
                    return False
        return True
    return False
    
            


def getLegalMoves(board, color,history):
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
                record = board.apply_move(move)

                king_pos = board.wking_pos if color == "white" else board.bking_pos
                if not isSquareAttacked(board, *king_pos, by_white=(color == "black")):
                    moves.append(move)

                board.undo_move(move, record)
    
    #CASTLING LOGIC

    row = 7 if color == "white" else 0
    king_start = (row, 4)

    # Kingside (SHORT) castling
    if canCastle(board, color, "SHORT", history):
        # King moves two squares right: e1 to g1 (white), e8 to g8 (black)
        moves.append((king_start, (row, 6)))
    # Queenside (LONG) castling
    if canCastle(board, color, "LONG", history):
        # King moves two squares left: e1 to c1 (white), e8 to c8 (black)
        moves.append((king_start, (row, 2)))

    return moves
