from board import WPAWN, WKNIGHT, WBISHOP, WROOK, WQUEEN, WKING
from board import EMPTY
from board import BPAWN, BKNIGHT, BBISHOP, BROOK, BQUEEN, BKING

def in_bounds(x, y):
	return 0 <= x < 8 and 0 <= y < 8

def pawn_moves(board, x, y, piece):
	moves = []
	direction = -1 if piece > 0 else 1

	nx, ny = x + direction, y

	if in_bounds(nx, ny) and board[nx][ny] == EMPTY:
		moves.append((nx, ny))

	for dy in [-1, 1]:
		nx, ny = x + direction, y + dy

		if in_bounds(nx, ny) and board[nx][ny] != EMPTY and board[nx][ny]*piece < 0:
			moves.append((nx, ny))

	return moves
