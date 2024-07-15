import sys
import Utility

def MiniMaxGame(board, depth, isMax):
    if depth == 0:
        return (1, Utility.static_estimation_midgame_endgame(board), [])

    if isMax:
        best_val = float('-inf')
        moves = Utility.generate_moves_midgame_endgame(board)
    else:
        best_val = float('inf')
        moves = Utility.generate_moves_midgame_endgame_for_black(board)

    best_move = []
    total_count = 0

    for move in moves:
        count, val, _ = MiniMaxGame(move, depth - 1, not isMax)
        total_count += count

        if isMax and val > best_val:
            best_val = val
            best_move = move
        elif not isMax and val < best_val:
            best_val = val
            best_move = move

    return (total_count, best_val, best_move)

def main():
    with open(sys.argv[1], 'r') as reader:
        startingBoard = reader.readline().strip()

    depth = int(sys.argv[2])
    board = [c for c in startingBoard]

    count, val, best_move = MiniMaxGame(board, depth, True)

    # Convert the board position list to a string for output
    board_position_str = ''.join(best_move)
    result = f"Board Position: {board_position_str}\nPositions evaluated by static estimation: {count}\nMINIMAX estimate: {val}\ndepth: {depth}"
    with open(sys.argv[3], 'w') as writer:
        writer.write(result)

if __name__ == "__main__":
    main()