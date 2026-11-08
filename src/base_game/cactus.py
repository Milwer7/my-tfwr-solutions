import nav
import actions

OPPOSITE = {North: South, East: West, South: North, West: East}

def plant_tile(arg):
	actions.tend(Entities.Cactus, False)
	return None

def wait_tile(arg):
	if get_entity_type() == Entities.Cactus:
		while not can_harvest():
			pass
	return None

def plant_region(x0, y0, size):
	for x in range(x0, x0 + size):
		for y in range(y0, y0 + size):
			nav.goto(x, y)
			actions.tend(Entities.Cactus, False)

def sort_line(x0, y0, length, d):
	back = OPPOSITE[d]
	end = length
	swapped = True
	while swapped and end > 1:
		swapped = False
		nav.goto(x0, y0)
		prev = measure()
		for i in range(end - 1):
			move(d)
			cur = measure()
			if prev > cur:
				swap(back)
				swapped = True
			else:
				prev = cur
		end -= 1

def line_worker(length, d):
	def work():
		sort_line(get_pos_x(), get_pos_y(), length, d)
	return work

def sort_lines(n, along, step):
	# one drone per line: sort along `along`, next line is one step in `step`
	nav.goto(0, 0)
	work = line_worker(n, along)
	drones = []
	for i in range(n):
		sx = get_pos_x()
		sy = get_pos_y()
		d = spawn_drone(work)
		if d == None:
			work()
			nav.goto(sx, sy)
		else:
			drones.append(d)
		move(step)
	for d in drones:
		wait_for(d)

def sort_region(x0, y0, size):
	for y in range(y0, y0 + size):
		sort_line(x0, y, size, East)
	for x in range(x0, x0 + size):
		sort_line(x, y0, size, North)

def wait_grown(x0, y0, size):
	for x in range(x0, x0 + size):
		for y in range(y0, y0 + size):
			nav.goto(x, y)
			if get_entity_type() == Entities.Cactus:
				while not can_harvest():
					pass
def run_region(x0, y0, size):
	plant_region(x0, y0, size)
	sort_region(x0, y0, size)
	wait_grown(x0, y0, size)
	nav.goto(x0, y0)
	harvest()
	

def run():
	n = get_world_size()
	nav.sweep(plant_tile)
	sort_lines(n, East, North)
	sort_lines(n, North, East)
	nav.sweep(wait_tile)
	nav.goto(0, 0)
	harvest()