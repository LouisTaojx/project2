import sys
import Utility

class BoardOut:
    def __init__(self):
        self.count = 0
        self.val = 0
        self.list = []

def ABPruning(board, depth, isMax, alpha, beta):
    out = BoardOut()
    if depth == 0:
        out.count += 1
        out.val = Utility.static_estimation_midgame_endgame(board)
        return out

    if isMax:
        moves = Utility.generate_moves_midgame_endgame(board)
    else:
        moves = Utility.generate_moves_midgame_endgame_for_black(board)

    for move in moves:
        if isMax:
            out2 = ABPruning(move, depth - 1, False, alpha, beta)
            out.count += out2.count
            if out2.val > alpha:
                out.list = move
                alpha = out2.val
        else:
            out2 = ABPruning(move, depth - 1, True, alpha, beta)
            out.count += out2.count
            if out2.val < beta:
                out.list = move
                beta = out2.val

        if alpha >= beta:
            break

    out.val = alpha if isMax else beta
    return out

def main():
    with open(sys.argv[1], 'r') as reader:
        startingBoard = reader.readline().strip()

    depth = int(sys.argv[2])
    board = [c for c in startingBoard]

    op = ABPruning(board, depth, True, float('-inf'), float('inf'))

    result = f"Board Position: {op.list}\nPositions evaluated by static estimation: {op.count}\nαβ estimate: {op.val}\ndepth: {depth}"
    with open(sys.argv[3], 'w', encoding='utf-8') as writer:  # Specify UTF-8 encoding here
        writer.write(result)

if __name__ == "__main__":
    main()