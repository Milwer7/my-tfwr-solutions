import nav

DIRS = [North, East, South, West]
DX = {North: 0, East: 1, South: 0, West: -1}
DY = {North: 1, East: 0, South: -1, West: 0}
OPPOSITE = {North: South, East: West, South: North, West: East}

# ---------- basics ----------

def here():
	return (get_pos_x(), get_pos_y())

def neighbor(pos, d):
	return (pos[0] + DX[d], pos[1] + DY[d])

def dist(a, b):
	return abs(a[0] - b[0]) + abs(a[1] - b[1])

def cost():
	return get_world_size() * 2 ** (num_unlocked(Unlocks.Mazes) - 1)

def create(amount):
	if get_entity_type() != Entities.Bush:
		harvest()
		plant(Entities.Bush)
	use_item(Items.Weird_Substance, amount)

# ---------- map knowledge ----------
# known[(x, y)] = {North: bool, East: bool, South: bool, West: bool}

def observe(known):
	# always refresh the current cell (walls can disappear on reuse)
	# and keep the mirrored side of already-known neighbors in sync
	pos = here()
	info = {}
	for d in DIRS:
		info[d] = can_move(d)
		nb = neighbor(pos, d)
		if nb in known:
			known[nb][OPPOSITE[d]] = info[d]
	known[pos] = info

def is_open(known, pos, d, n):
	nb = neighbor(pos, d)
	if nb[0] < 0 or nb[0] >= n or nb[1] < 0 or nb[1] >= n:
		return False
	if pos in known:
		return known[pos][d]
	if nb in known:
		return known[nb][OPPOSITE[d]]
	return True  # unknown: assume open, replan if wrong

def merge_known(into, part):
	for pos in part:
		into[pos] = part[pos]

# ---------- workers ----------

def wait_for_maze(max_checks=1000000):
	checks = 0
	while get_entity_type() != Entities.Hedge and get_entity_type() != Entities.Treasure:
		checks += 1
		if checks > max_checks:
			return False
	return True

def explore(lo, hi):
	# DFS restricted to columns lo..hi-1, records every visited cell's open sides
	known = {}
	observe(known)
	visited = {here(): True}
	path = []
	while True:
		pos = here()
		moved = False
		for d in DIRS:
			nb = neighbor(pos, d)
			if lo <= nb[0] and nb[0] < hi and not (nb in visited) and known[pos][d]:
				move(d)
				visited[nb] = True
				path.append(d)
				observe(known)
				moved = True
				break
		if not moved:
			if len(path) == 0:
				return known
			move(OPPOSITE[path.pop()])

def mapper(lo, hi):
	def work():
		if not wait_for_maze():
			return {}
		return explore(lo, hi)
	return work

def strips(n, k):
	out = []
	w = (n + k - 1) // k
	x = 0
	while x < n:
		x1 = min(x + w, n)
		out.append((x, x1))
		x = x1
	return out

def widen(r, margin, n):
	# let a strip's DFS spill into its neighbors so paths that
	# leave the strip and come back are still mapped
	return (max(0, r[0] - margin), min(n, r[1] + margin))

# ---------- binary heap (entries are (key, pos), ordered by key) ----------

def heap_push(h, item):
	h.append(item)
	i = len(h) - 1
	while i > 0:
		p = (i - 1) // 2
		if h[p][0] <= h[i][0]:
			break
		tmp = h[p]
		h[p] = h[i]
		h[i] = tmp
		i = p

def heap_pop(h):
	top = h[0]
	last = h.pop()
	size = len(h)
	if size > 0:
		h[0] = last
		i = 0
		while True:
			l = 2 * i + 1
			r = l + 1
			s = i
			if l < size and h[l][0] < h[s][0]:
				s = l
			if r < size and h[r][0] < h[s][0]:
				s = r
			if s == i:
				break
			tmp = h[s]
			h[s] = h[i]
			h[i] = tmp
			i = s
	return top

# ---------- A* ----------

def reconstruct(came, cur):
	rev = []
	while cur in came:
		step = came[cur]
		rev.append(step[1])
		cur = step[0]
	path = []
	i = len(rev) - 1
	while i >= 0:
		path.append(rev[i])
		i -= 1
	return path

def astar(start, goal, known, n):
	# key = f * scale - g: orders by f, breaks ties toward deeper nodes
	scale = n * n + 1
	heap = []
	heap_push(heap, (dist(start, goal) * scale, start))
	g = {start: 0}
	came = {}
	closed = {}
	while len(heap) > 0:
		cur = heap_pop(heap)[1]
		if cur in closed:
			continue  # stale entry
		if cur == goal:
			return reconstruct(came, cur)
		closed[cur] = True
		for d in DIRS:
			if is_open(known, cur, d, n):
				nb = neighbor(cur, d)
				if nb in closed:
					continue
				ng = g[cur] + 1
				if not (nb in g) or ng < g[nb]:
					g[nb] = ng
					came[nb] = (cur, d)
					heap_push(heap, ((ng + dist(nb, goal)) * scale - ng, nb))
	return None

def go_to(goal, known, n):
	# follow the A* path, refreshing walls on the way and replanning when blocked
	observe(known)
	while here() != goal:
		path = astar(here(), goal, known, n)
		if path == None:
			return False
		for d in path:
			if not known[here()][d]:
				break  # observe just found a wall the plan assumed open
			move(d)
			observe(known)
	return True

# ---------- main routine ----------

def run(reuses=10, margin=2):
	n = get_world_size()
	regions = strips(n, max_drones())

	# place one mapper per strip; the main drone keeps the last strip
	drones = []
	for i in range(len(regions) - 1):
		r = regions[i]
		nav.goto(r[0], 0)
		w = widen(r, margin, n)
		d = spawn_drone(mapper(w[0], w[1]))
		if d != None:
			drones.append(d)

	last = regions[len(regions) - 1]
	nav.goto(last[0], 0)
	create(cost())

	w = widen(last, margin, n)
	known = explore(w[0], w[1])
	for d in drones:
		merge_known(known, wait_for(d))

	# chase the treasure, reusing the maze while substance lasts
	for i in range(reuses):
		go_to(measure(), known, n)
		if num_items(Items.Weird_Substance) < cost():
			break
		use_item(Items.Weird_Substance, cost())
	go_to(measure(), known, n)
	harvest()