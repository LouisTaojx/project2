import sys
from typing import List
import Utility
from Utility import *


def MinMaxOpening(board, depth, is_max):
    out = BoardOut()
    if depth == 0:
        out.count += 1
        out.val = Utility.static_estimation_for_opening(board)
        return out

    if is_max:
        out.val = -float('inf')
        moves = Utility.generate_moves_opening(board)
    else:
        out.val = float('inf')
        moves = Utility.generate_moves_opening_for_black(board)

    for list in moves:
        if is_max:
            out2 = MinMaxOpening(list, depth - 1, False)
        else:
            out2 = MinMaxOpening(list, depth - 1, True)

        out.count += out2.count
        if is_max and out2.val > out.val:
            out.list = list
            out.val = out2.val
        elif not is_max and out2.val < out.val:
            out.list = list
            out.val = out2.val

    return out

if __name__ == "__main__":
    with open(sys.argv[1], 'r') as reader:
        starting_board = reader.readline().strip()
    depth = int(sys.argv[2])
    ip = list(starting_board)
    op = MinMaxOpening(Utility.PosList(ip), depth, True)

    result = f"Board Position: {op.list}\nPositions evaluated by static estimation: {op.count}\nMINIMAX estimate: {op.val}\ndepth: {depth}"
    with open(sys.argv[3], 'w') as writer:
        writer.write(result)
