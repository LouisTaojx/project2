import sys
import Utility

class BoardOut:
    def __init__(self):
        self.count = 0
        self.val = 0
        self.list = []

def MinMaxOpening(board, depth, is_max):
    out = BoardOut()
    if depth == 0:
        out.count += 1
        out.val = Utility.static_estimation_for_opening(board) # board is a list of Position
        return out

    if is_max:
        out.val = -float('inf')
        moves = Utility.generate_add(board)
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
        read_board = reader.readline().strip()
    depth = int(sys.argv[2])
    board = list(read_board)

    next_move = MinMaxOpening(board, depth, True)
    # write the result to the output file
    result = f"Board Position: {next_move.list}\nPositions evaluated by static estimation: {next_move.count}\nMINIMAX estimate: {next_move.val}\ndepth: {depth}"
    with open(sys.argv[3], 'w') as writer:
        writer.write(result)

