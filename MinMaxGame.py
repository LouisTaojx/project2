import sys
import Utility

class BoardOut:
    def __init__(self):
        self.count = 0
        self.val = 0
        self.list = []

def MiniMaxGame(board, depth, isMax):
    out = BoardOut()

    if depth == 0:
        out.count += 1
        out.val = Utility.static_estimation_midgame_endgame(board)  
        return out

    if isMax:
        out.val = float('-inf')
        moves = Utility.generate_moves_midgame_endgame(board) 
    else:
        out.val = float('inf')
        moves = Utility.generate_moves_midgame_endgame_for_black(board) 

    for move in moves:
        if isMax:
            out2 = MiniMaxGame(move, depth - 1, False)
            out.count += out2.count
            if out2.val > out.val:
                out.list = move
                out.val = out2.val
        else:
            out2 = MiniMaxGame(move, depth - 1, True)
            out.count += out2.count
            if out2.val < out.val:
                out.list = move
                out.val = out2.val

    return out

def main():
    with open(sys.argv[1], 'r') as reader:
        startingBoard = reader.readline().strip()

    depth = int(sys.argv[2])
    board = [c for c in startingBoard]

    op = MiniMaxGame(board, depth, True)

    result = f"Board Position: {op.list}\nPositions evaluated by static estimation: {op.count}\nMINIMAX estimate: {op.val}\ndepth: {depth}"
    with open(sys.argv[3], 'w') as writer:
        writer.write(result)

if __name__ == "__main__":
    main()