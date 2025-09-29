from src.backend.api import API
import random

api = API()

state = api.get_state()
print(state["board"])  # 8x8 int matrix of pieces
print(state["turn"])  # "white" or "black"
print(state["over"])  # True/False
print(state["result"])  # e.g. "checkmate_white", "stalemate", or None

# get the list of legal moves in ((fx, fy), (tx, ty)) form
moves = api.get_legal_moves()

# apply move (returns MoveRecord)
record = api.apply_move(moves[0])

# undo move
api.undo_move(moves[0], record)

# make a move (validated)
# uses internal validation and updates turn/history
record = api.make_move(moves[0])
if record is None:
    print("illegal move")


# get current board
board = api.get_board()

api = API()
while not api.get_state()["over"]:
    print(api.get_board())
    moves = api.get_legal_moves()
    if api.get_state()["turn"] == "white":
        idx = int(input(f"Choose move [0-{len(moves)-1}]: "))
        api.make_move(moves[idx])
    else:
        move = random.choice(moves)
        api.make_move(move)
