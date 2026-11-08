import nav
import drone_config

DX = {North: 0, East: 1, South: 0, West: -1}
DY = {North: 1, East: 0, South: -1, West: 0}
DIRS = [North, East, South, West]

# ---------- Hamiltonian cycle ----------
# Columns zigzag over rows 1..n-1, row 0 is the return lane:
#   (0,0) up column 0, down column 1, up column 2, ... down the last column,
#   then west along row 0 back to (0,0).
# Needs an even number of columns, so on an odd farm the last column is unused.

def cycle_width(n):
	if n % 2 == 0:
		return n
	return n - 1

def build_cycle(n):
	w = cycle_width(n)
	order = [(0, 0)]
	for x in range(w):
		if x % 2 == 0:
			for y in range(1, n):
				order.append((x, y))
		else:
			y = n - 1
			while y >= 1:
				order.append((x, y))
				y -= 1
	x = w - 1
	while x >= 1:
		order.append((x, 0))
		x -= 1
	idx = {}
	for i in range(len(order)):
		idx[order[i]] = i
	return order, idx

def step_dir(a, b):
	for d in DIRS:
		if a[0] + DX[d] == b[0] and a[1] + DY[d] == b[1]:
			return d
	return None

# ---------- helpers ----------

def here():
	return (get_pos_x(), get_pos_y())

def ahead(idx, a, b, size):
	# how many cycle steps from a forward to b
	return (idx[b] - idx[a]) % size

def clear_tile(arg):
	if get_entity_type() != None:
		harvest()
	return None

def choose(head, apple, body, order, idx, size):
	# default: follow the cycle, which can never trap the snake
	nxt = order[(idx[head] + 1) % size]
	best = step_dir(head, nxt)
	if apple == None or not (apple in idx):
		return best
	# shortcuts only while the snake is short enough to leave room
	if len(body) * 2 > size:
		return best
	if len(body) > 0:
		to_tail = ahead(idx, head, body[0], size)
	else:
		to_tail = size
	to_apple = ahead(idx, head, apple, size)
	margin = 4
	best_jump = 1
	for d in DIRS:
		nb = (head[0] + DX[d], head[1] + DY[d])
		if not (nb in idx):
			continue
		jump = ahead(idx, head, nb, size)
		# skip forward on the cycle, never past the apple, never near the tail
		if jump > best_jump and jump <= to_apple and jump < to_tail - margin:
			if can_move(d):
				best = d
				best_jump = jump
	return best

# ---------- main routine ----------

def run(max_apples=100000):
	n = get_world_size()
	order, idx = build_cycle(n)
	size = len(order)

	# empty farm, start of the cycle, then become a dinosaur
	nav.sweep(clear_tile)
	nav.goto(0, 0)
	change_hat(Hats.Dinosaur_Hat)

	apple = measure()  # None if the apple can't be read from here yet
	body = []  # tail pieces, oldest first
	eaten = 0
	idle = 0  # moves since the last apple

	while eaten < max_apples and len(body) < size - 1:
		head = here()
		d = choose(head, apple, body, order, idx, size)
		if not move(d):
			break  # boxed in: should not happen on the cycle
		body.append(head)
		# a new apple position means the previous one was just eaten
		m = measure()
		ate = m != None and m != apple
		if ate:
			apple = m
			eaten += 1
			idle = 0
		else:
			body.pop(0)
			idle += 1
			# a full lap without food: no more apples (out of cactus, or farm full)
			if idle > size:
				break

	# taking the hat off harvests the tail into bones
	drone_config.init()
	return eaten