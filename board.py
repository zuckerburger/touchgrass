EMPTY = 0
WPAWN, WKNIGHT, WBISHOP, WROOK, WQUEEN, WKING = 1, 2, 3, 4, 5, 6
BPAWN, BKNIGHT, BBISHOP, BROOK, BQUEEN, BKING = -1, -2, -3, -4, -5, -6


class Board:
	def __init__(self):
		self.board = self.starting_pos()
		self.wking_pos = (7, 4)
		self.bking_pos = (0, 4)

	def starting_pos(self):
		return [
			[BROOK, BKNIGHT, BBISHOP, BQUEEN, BKING, BBISHOP, BKNIGHT, BROOK],
			[BPAWN, BPAWN, BPAWN, EMPTY, BPAWN, BPAWN, BPAWN, BPAWN],
			[EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
			[EMPTY, EMPTY, EMPTY, BPAWN, EMPTY, EMPTY, EMPTY, EMPTY],
			[EMPTY, EMPTY, EMPTY, EMPTY, WPAWN, EMPTY, EMPTY, EMPTY],
			[EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
			[WPAWN, WPAWN, WPAWN, WPAWN, EMPTY, WPAWN, WPAWN, WPAWN],
			[WROOK, WKNIGHT, WBISHOP, WQUEEN, WKING, WBISHOP, WKNIGHT, WROOK]
		]

	def apply_move(self, move):
		(fx, fy), (tx, ty) = move

		piece = self.board[fx][fy]

		captured = self.board[tx][ty]

		self.board[tx][ty] = piece
		self.board[fx][fy] = EMPTY

		if piece == WKING:
			self.whking_pos = (tx, ty)
		elif piece == BKING:
			self.bking_pos = (tx, ty)

		return captured

	def undo_move(self, move, captured):
		(fx, fy), (tx, ty) = move
		piece = self.board[tx][ty]

		self.board[fx][fy] = piece
		self.board[tx][ty] = captured

		if piece == WKING:
			self.wking_pos = (fx, fy)
		elif piece == BKING:
			self.bking_pos = (fx, fy)
