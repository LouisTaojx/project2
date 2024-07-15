import sys
import Utility  

def ABPruning(board, depth, isMax, alpha, beta):
	count = 0
	# best_val = float('-inf') if isMax else float('inf')
	best_move = None

	if depth == 0:
		count += 1
		val = Utility.static_estimation_for_opening(board)
		return (count, val, [])

	if isMax:
		moves = Utility.generate_add(board)
	else:
		moves = Utility.generate_moves_opening_for_black(board)

	for move in moves:
		out2_count, out2_val, _ = ABPruning(move, depth-1, not isMax, alpha, beta)
		count += out2_count

		if isMax and out2_val > alpha:
			best_move = move
			alpha = out2_val
		elif not isMax and out2_val < beta:
			best_move = move
			beta = out2_val

		if alpha >= beta:
			break

	val = alpha if isMax else beta
	return (count, val, best_move)


def main(input_file, depth, output_file):
	with open(input_file, 'r') as reader:
		startingBoard = reader.readline().strip()
	board = [c for c in startingBoard]

	count, val, best_move = ABPruning(board, int(depth), True, float('-inf'), float('inf'))
    
	result = f"Board Position: {''.join(best_move)}\nPositions evaluated by static estimation: {count}\n αβ estimate: {val}\ndepth: {depth}"
	with open(output_file, 'w', encoding='utf-8') as writer:
		writer.write(result)
	


if __name__ == "__main__":
	main(sys.argv[1], sys.argv[2], sys.argv[3])

