from board import Board
from move_gen import getLegalMoves


def printBoard(board):
	for row in board:
		print(' '.join(f'{p:2}' for p in row))
	print()

def main():
	p = Board()
	turn = 'white'
	printBoard(p.board)

	moves = getLegalMoves(p, turn)

	print(f"{turn} has {len(moves)} legal moves:")
	for m in moves:
		print(m)

main()
