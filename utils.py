# warning: clanker slop

piece_map = {
    0: ".",
    1: "P",
    2: "N",
    3: "B",
    4: "R",
    5: "Q",
    6: "K",
    -1: "p",
    -2: "n",
    -3: "b",
    -4: "r",
    -5: "q",
    -6: "k",
}


def print_board(board):
    print("   a b c d e f g h")
    for i, row in enumerate(board):
        rank = 8 - i
        print(f"{rank}  " + " ".join(piece_map[p] for p in row) + f"  {rank}")
    print("   a b c d e f g h\n")
