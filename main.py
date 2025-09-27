from api import API
from utils import print_board


def coord(square):
    file = ord(square[0].lower()) - ord("a")
    rank = 8 - int(square[1])
    return (rank, file)


def main():
    game = API()

    while not game.get_state()["over"]:
        print_board(game.get_state()["board"])
        move_str = input(f"{game.get_state()['turn']}'s move: ")
        move = (coord(move_str[:2]), coord(move_str[2:]))
        game.play(move)

    print("Game Over:", game.get_state()["result"])


if __name__ == "__main__":
    main()
