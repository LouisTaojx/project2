import sys
import Utility

def ABPruning(board, depth, isMax, alpha, beta):
    if depth == 0:
        return (1, Utility.static_estimation_midgame_endgame(board), [])

    best_move = []
    total_count = 0
    val = float('-inf') if isMax else float('inf')

    moves = Utility.generate_moves_midgame_endgame(board) if isMax else Utility.generate_moves_midgame_endgame_for_black(board)

    for move in moves:
        count, move_val, _ = ABPruning(move, depth - 1, not isMax, alpha, beta)
        total_count += count

        if isMax:
            if move_val > alpha:
                alpha = move_val
                best_move = move
            val = alpha
        else:
            if move_val < beta:
                beta = move_val
                best_move = move
            val = beta

        if alpha >= beta:
            break

    return (total_count, val, best_move)

def main():
    with open(sys.argv[1], 'r') as reader:
        startingBoard = reader.readline().strip()

    depth = int(sys.argv[2])
    board = [c for c in startingBoard]

    count, val, best_move = ABPruning(board, depth, True, float('-inf'), float('inf'))

    board_position_str = ''.join(best_move)
    result = f"Board Position: {board_position_str}\nPositions evaluated by static estimation: {count}\nαβ estimate: {val}\ndepth: {depth}"
    with open(sys.argv[3], 'w', encoding='utf-8') as writer:
        writer.write(result)

if __name__ == "__main__":
    main()