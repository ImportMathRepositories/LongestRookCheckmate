# Classifies all unsorted positions by mate in x

import position_util

# Identifies and relocates unsorted white positions that belong in the next mating depth
def white_to_move(mating_depths, unsorted_white, unsorted_black):
	# Loop ends when no there are no positions left to sort
	if unsorted_white:
		mating_depths.append(set())
		for i in range(len(unsorted_white) - 1, -1, -1):
			for current_pos in unsorted_white[i][1]:
				if current_pos in mating_depths[-2]:
					transitional_pos = unsorted_white.pop(i)
					mating_depths[-1].add(str(transitional_pos[0]))
					break

		# Print the result and continue to black's move
		print_result(len(mating_depths) - 1, len(mating_depths[-1]))
		black_to_move(mating_depths, unsorted_white, unsorted_black)
	else:
		print_final_result(len(mating_depths) - 1)

# Identifies and relocates unsorted black positions that belong in the next mating depth
def black_to_move(mating_depths, unsorted_white, unsorted_black):
	# Generate a set of the current unsorted white list for better lookup
	unsorted_white_set = set()
	for current_white in unsorted_white:
		unsorted_white_set.add(str(current_white[0]))

	# Loop ends when no there are no positions left to sort
	if unsorted_black:
		mating_depths.append(set())
		for i in range(len(unsorted_black) - 1, -1, -1):
			getting_mated = True
			for current_pos in unsorted_black[i][1]:
				if current_pos in unsorted_white_set:
					getting_mated = False
					break
			if getting_mated:
				transitional_pos = unsorted_black.pop(i)
				mating_depths[-1].add(str(transitional_pos[0]))

		# Print the result and continue to white's move
		print_result(len(mating_depths) - 1, len(mating_depths[-1]))
		white_to_move(mating_depths, unsorted_white, unsorted_black)
	else:
		print_final_result(len(mating_depths) - 1)

# Calculates all of the moves for each of the unsorted positions, regardless of legality
def solve_prep(mating_depths, unsorted_white, unsorted_black):
	for i in range(len(unsorted_white)):
		current_pos = unsorted_white[i]
		unsorted_white[i] = [current_pos, position_util.get_white_moves(current_pos)]
	for i in range(len(unsorted_black)):
		current_pos = unsorted_black[i]
		unsorted_black[i] = [current_pos, position_util.get_black_moves(current_pos)]

	# Print the mate in 0 results and begin the full classification loop
	print_result(len(mating_depths) - 1, len(mating_depths[-1]))
	white_to_move(mating_depths, unsorted_white, unsorted_black)

# Print the results of the current depth
def print_result(d, n):
	print('Mate in ' + str(d) + ': ' + str(n))

# Print the final answer to the problem
def print_final_result(n):
	print('White can checkmate in ' + str(n) + ' half moves or less')
