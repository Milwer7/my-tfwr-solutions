dims = get_world_size()

def make_board(n, fill=None):
	board = []
	for x in range(n):
		col = []
		for y in range(n):
			col.append(fill)
		board.append(col)
	return board
	
def fill_rows(board, entities, period=1, offset=0):
	# row y gets entities[(y // period + offset) % len(entities)]
	n = len(board)
	for x in range(n):
		for y in range(n):
			board[x][y] = entities[(y // period + offset) % len(entities)]

def fill_columns(board, entities, period=1, offset=0):
	n = len(board)
	for x in range(n):
		for y in range(n):
			board[x][y] = entities[(x // period + offset) % len(entities)]

def fill_checker(board, a, b):
	n = len(board)
	for x in range(n):
		for y in range(n):
			if (x + y) % 2 == 0:
				board[x][y] = a
			else:
				board[x][y] = b
				
def fill_from(board, layout_fn):
	n = len(board)
	for x in range(n):
		for y in range(n):
			board[x][y] = layout_fn(x, y)

def positions_of(board, entity):
	out = []
	n = len(board)
	for x in range(n):
		for y in range(n):
			if board[x][y] == entity:
				out.append((x, y))
	return out