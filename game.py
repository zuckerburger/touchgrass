from board import Board
import random
from move_gen import getLegalMoves

class Game:
	def __init__(self):
		self.board = Board()
		self.turn = 'white'

	def legal_moves(self):
		return getLegalMoves(self.board, self.turn)

	def make_move(self, move):
		captured = self.board.apply_move(move)

		self.turn = 'black' if self.turn == 'white' else 'white'

		return captured

	def play_random(self):
		moves = self.legal_moves()

		if not moves:
			return None

		move = random.choice(moves)

		self.make_move(move)
		return move
