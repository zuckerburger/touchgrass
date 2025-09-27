# from board import Board
# from move_gen import getLegalMoves
from game import Game

def move_coord(square):
	return (8 - int(square[1]), ord(square[0].lower()) - ord('a'))

def printBoard(board):
	for row in board.board:
		print(' '.join(f'{p:2}' for p in row))
	print()

def main():
	'''
	p = Board()
	turn = 'white'
	printBoard(p.board)

	moves = getLegalMoves(p, turn)

	print(f"{turn} has {len(moves)} legal moves:")
	for m in moves:
		print(m)
	'''

	g = Game()
	printBoard(g.board)

	while True:
		moves = g.legal_moves()
		if not moves:
			print(f"no legal moves for {g.turn}. GAME OVER.")
			break

		if g.turn == 'white':
			# print(moves)
			the_move = input('move: ').strip().split()
			source, destination = the_move
			move = (move_coord(source), move_coord(destination))
			if move not in moves:
				print('illegal')
				continue
			g.make_move(move)
			print(f"white plays: {move}")

		else:
			move = g.play_random()
			print(f"black plays: {move}")

		printBoard(g.board)



main()
