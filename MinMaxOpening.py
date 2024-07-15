import sys
import Utility
# for improving the performance of the code, I did some optimization. 
def MinMaxOpening(board, depth, is_max):
	if depth == 0:
		val = Utility.static_estimation_for_opening(board)
		return (1, val, board)  # count, val, list

	best_move = None
	if is_max:
		best_val = -float('inf')
		moves = Utility.generate_add(board)
	else:
		best_val = float('inf')
		moves = Utility.generate_moves_opening_for_black(board)

	total_count = 0
	for current_move in moves:
		count, val, _ = MinMaxOpening(current_move, depth - 1, not is_max)
		total_count += count

		if is_max and val > best_val:
			best_val = val
			best_move = current_move
		elif not is_max and val < best_val:
			best_val = val
			best_move = current_move

	return (total_count, best_val, best_move)

if __name__ == "__main__":
	with open(sys.argv[1], 'r') as reader:
		read_board = reader.readline().strip()
	depth = int(sys.argv[2])
	board = list(read_board)

	count, val, next_move = MinMaxOpening(board, depth, True)
	next_move = ''.join(next_move)
	result = f"Board Position: {next_move}\nPositions evaluated by static estimation: {count}\nMINIMAX estimate: {val}\ndepth: {depth}"
	with open(sys.argv[3], 'w') as writer:
		writer.write(result)
