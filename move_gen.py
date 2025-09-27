from pieces import pawn_moves
from board import WKING, BKING, WPAWN, EMPTY

def getPseudoLegalMoves(board, x, y):
	piece = board[x][y]
	if piece == EMPTY:
		return []
	if abs(piece) == WPAWN:
		return pawn_moves(board, x, y, piece)
	return []


def isSquareAttacked(board, x, y, by_white):
	for i in range(8):
		for j in range(8):
			piece = board.board[i][j]
			if piece == 0:
				continue
			if by_white and piece <= 0:
				continue

			if not by_white and piece >= 0:
				continue
			for nx, ny in getPseudoLegalMoves(board.board, i, j):
				if nx == x and ny == y:
					return True
		return False

def getLegalMoves(board, color):
	moves = []

	for x in range(8):
		for y in range(8):
			piece = board.board[x][y]
			if piece == 0:
				continue
			if color == 'white' and piece < 0:
				continue
			if color == 'black' and piece > 0:
				continue

			for nx, ny in getPseudoLegalMoves(board.board, x, y):
				move = ((x, y), (nx, ny))
				captured = board.apply_move(move)

				king_pos = board.wking_pos if color == 'white' else board.bking_pos
				if not isSquareAttacked(board, *king_pos, by_white=(color == ' black')):
					moves.append(move)
				board.undo_move(move, captured)

	return moves
