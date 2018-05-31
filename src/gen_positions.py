# Generates and filters the initial positions

import position_util
import solve

# Piece keys
BLACK_KING = 'black_king'
WHITE_KING = 'white_king'
WHITE_ROOK = 'white_rook'

# Constant integers
TOTAL_POSITIONS = 64 * 63 * 62 * 2
BOARD_WIDTH = 8

# Global data structures
unsorted_white = []
unsorted_black = []
mating_depths = [set()]

# Global counters (strictly for information purposes)
illegal_count = 0
immediate_capture_count = 0
stalemate_count = 0

# Places the black king in every position in preparation for the white king
def place_black_king():
	for x in range(BOARD_WIDTH):
		for y in range(BOARD_WIDTH):
			place_white_king({BLACK_KING: [x, y]})

# Places the white king in every legal position in preparation for the white rook
def place_white_king(position):
	black_king = position[BLACK_KING]

	for x in range(BOARD_WIDTH):
		for y in range(BOARD_WIDTH):
			if not position_util.adjacent(black_king, [x, y]):
				place_white_rook({BLACK_KING: black_king, WHITE_KING: [x, y]})

# Places the white rook, but does not check for legality
def place_white_rook(position):
	black_king = position[BLACK_KING]
	white_king = position[WHITE_KING]

	for x in range(BOARD_WIDTH):
		for y in range(BOARD_WIDTH):
			if black_king != [x, y] and white_king != [x, y]:
				side_to_move({BLACK_KING: black_king, WHITE_KING: white_king, WHITE_ROOK: [x, y]})

# Branches each position for white to move and black to move
def side_to_move(position):
	white_filters(position)
	black_filters(position)

# Checks for immediate rook captures
def white_filters(position):
	if position_util.rook_can_capture_king(position):
		global illegal_count
		illegal_count += 1
	else:
		unsorted_white.append(position)

# Checks for illegal positions and stalemates. Also classifies mate in 0 positions
def black_filters(position):
	if position_util.king_can_capture_rook(position):
		global immediate_capture_count
		immediate_capture_count += 1
	elif position_util.no_legal_moves(position):
		if position_util.rook_can_capture_king(position):
			mating_depths[0].add(str(position))
		else:
			global stalemate_count
			stalemate_count += 1
	else:
		unsorted_black.append(position)

# Printing initial information
print('Total positions: ' + str(TOTAL_POSITIONS))
print('Building now...')

# Generate all of the positions
place_black_king()

# Print results of positions that were generated
print('Illegal: ' + str(TOTAL_POSITIONS - immediate_capture_count - stalemate_count - len(mating_depths[0]) - len(unsorted_white) - len(unsorted_black)))
print('King captures rook: ' + str(immediate_capture_count))
print('Stalemates: ' + str(stalemate_count))
print('Solving now...')

# Begin classifying the unsorted positions
solve.solve_prep(mating_depths, unsorted_white, unsorted_black)
