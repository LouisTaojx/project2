import sys
from Utility import static_estimation_midgame_endgame, generate_moves_midgame_endgame, generate_moves_midgame_endgame_for_black

def MiniMaxGameBlack(board, depth, is_max):
	if depth == 0:
		return (1, static_estimation_midgame_endgame(board), [])

	if is_max:
		val = float('-inf')
		moves = generate_moves_midgame_endgame(board)
	else: # is_max == False enter this line
		val = float('inf')
		moves = generate_moves_midgame_endgame_for_black(board)

	best_move = None
	total_count = 0

	for move in moves:
		out2_count, out2_val, _ = MiniMaxGameBlack(move, depth - 1, not is_max)
		total_count += out2_count

		if is_max and out2_val > val:
			best_move, val = move, out2_val
		elif not is_max and out2_val < val:
			best_move, val = move, out2_val

	return (total_count, val, best_move)

def main():
	with open(sys.argv[1], 'r') as reader:
		startingBoard = reader.readline().strip()

	depth = int(sys.argv[2])
	board = [c for c in startingBoard]  # Convert string to list of characters

	count, val, best_move = MiniMaxGameBlack(board, depth, False)

	result = f"Board Position: {''.join(best_move)}\nPositions evaluated by static estimation: {count}\nMINIMAX estimate: {val}\ndepth: {depth}"
	with open(sys.argv[3], 'w') as writer:
		writer.write(result)

if __name__ == "__main__":
	main()