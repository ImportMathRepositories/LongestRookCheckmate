# Contains simple utility functions to make working with positions easier

# Piece keys
BLACK_KING = 'black_king'
WHITE_KING = 'white_king'
WHITE_ROOK = 'white_rook'

# Constant integer
BOARD_WIDTH = 8

# Check if a square is on board (nothing outside of 0 and 7)
def on_board(a):
	return a[0] >= 0 and a[0] < BOARD_WIDTH and a[1] >= 0 and a[1] < BOARD_WIDTH

# Check for adjacency of two squares (diagonals count)
def adjacent(a, b):
	return abs(a[0] - b[0]) <= 1 and abs(a[1] - b[1]) <= 1

# Checks if b is between a and c
def piece_in_middle(a, b, c):
	if b > a and b > c:
		return False
	elif b < a and b < c:
		return False
	else:
		return True

# Checks if an undefended rook can be captured by the black king
def king_can_capture_rook(position):
	black_king = position[BLACK_KING]
	white_king = position[WHITE_KING]
	white_rook = position[WHITE_ROOK]

	if adjacent(black_king, white_rook):
		return not adjacent(white_king, white_rook)
	else:
		return False

# Checks to see if the white rook and capture the black king
def rook_can_capture_king(position):
	black_king = position[BLACK_KING]
	white_king = position[WHITE_KING]
	white_rook = position[WHITE_ROOK]

	if white_rook[0] == black_king[0]:
		if white_king[0] == white_rook[0]:
			return not piece_in_middle(white_rook[1], white_king[1], black_king[1])
		else:
			return True
	elif white_rook[1] == black_king[1]:
		if white_king[1] == white_rook[1]:
			return not piece_in_middle(white_rook[0], white_king[0], black_king[0])
		else:
			return True
	else:
		return False

# Checks to see if the black king can make any legal moves
def no_legal_moves(position):
	black_king = position[BLACK_KING]
	white_king = position[WHITE_KING]
	white_rook = position[WHITE_ROOK]

	if black_king[0] == 0 or black_king[0] == BOARD_WIDTH - 1 or black_king[1] == 0 or black_king[1] == BOARD_WIDTH - 1:
		for x in range(-1, 2):
			for y in range(-1, 2):
				if not x == 0 or not y == 0:
					new_black_king = [black_king[0] + x, black_king[1] + y]
					if on_board(new_black_king):
						new_position = {BLACK_KING: new_black_king, WHITE_KING: white_king, WHITE_ROOK: white_rook}
						if not adjacent(new_black_king, white_king) and not rook_can_capture_king(new_position):
							return False
		return True
	else:
		return False

# Gets a list of all moves for white, but does not check for legality
def get_white_moves(pos):
	black_king = pos[BLACK_KING]
	white_king = pos[WHITE_KING]
	white_rook = pos[WHITE_ROOK]

	moves = []

	# King moves
	for x in range(-1, 2):
		for y in range(-1, 2):
			if not x == 0 or not y == 0:
				new_white_king = [white_king[0] + x, white_king[1] + y]
				if on_board(new_white_king):
					moves.append(str({BLACK_KING: black_king, WHITE_KING: new_white_king, WHITE_ROOK: white_rook}))

	# Rook moves
	for increment in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
		i = 1
		while True:
			current_pos = [white_rook[0] + i * increment[0], white_rook[1] + i * increment[1]]
			if on_board(current_pos) and current_pos != white_king and current_pos != black_king:
				moves.append(str({BLACK_KING: black_king, WHITE_KING: white_king, WHITE_ROOK: current_pos}))
				i += 1
			else:
				break

	return moves

# Gets a list of all moves for black, but does not check for legality
def get_black_moves(pos):
	black_king = pos[BLACK_KING]
	white_king = pos[WHITE_KING]
	white_rook = pos[WHITE_ROOK]

	moves = []

	# King moves
	for x in range(-1, 2):
		for y in range(-1, 2):
			if not x == 0 or not y == 0:
				new_black_king = [black_king[0] + x, black_king[1] + y]
				if on_board(new_black_king):
					moves.append(str({BLACK_KING: new_black_king, WHITE_KING: white_king, WHITE_ROOK: white_rook}))

	return moves
