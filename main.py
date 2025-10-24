# from src.engine.minmax import MinimaxEngine
from src.engine.dumbo import DumboEngine
from src.backend.api import API
from src.utils import print_board, clear_screen, coords_to_uci

api = API()
engine = DumboEngine(api)
move_number = 1

last_engine_move = None

while not api.get_state()["over"]:
    state = api.get_state()

    clear_screen()
    print(f"\nMove {move_number} - {state['turn'].upper()}'s turn")
    print_board(state["board"])
    if last_engine_move:
        print(f"Last Engine Move: {last_engine_move}")

    if state["turn"] == "white":
        moves = api.get_legal_moves()
        for idx, move in enumerate(moves):
            print(f"{idx}: {coords_to_uci(move)}", end="  ")
        print()
        while True:
            try:
                choice = int(input(f"Choose move [0-{len(moves)-1}]: "))
                if 0 <= choice < len(moves):
                    api.make_move(moves[choice])
                    break
                print("Invalid choice, try again.")
            except ValueError:
                print("Invalid input, enter a number.")
    else:
        print("Engine Thinking...", end="", flush=True)
        move = engine.get_best_move()
        if move:
            api.make_move(move)
            # print(f"\rEngine plays: {coords_to_uci(move)}")
            last_engine_move = coords_to_uci(move)
        else:
            print("Engine has no Legal Moves!")
            break

    move_number += 1

clear_screen()
state = api.get_state()
print("\nGAME OVER")
print_board(state["board"])
print(f"Result: {state['result']}")
