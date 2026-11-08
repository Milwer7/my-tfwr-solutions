def shortest(cur, target, n):
	d = target - cur
	if abs(d) > n // 2:
		if d > 0:
			d -= n
		else:
			d += n
	return d

def goto(tx, ty):
	n = get_world_size()
	dx = shortest(get_pos_x(), tx, n)
	dy = shortest(get_pos_y(), ty, n)
	while dx > 0:
		move(East)
		dx -= 1
	while dx < 0:
		move(West)
		dx += 1
	while dy > 0:
		move(North)
		dy -= 1
	while dy < 0:
		move(South)
		dy += 1
		


def column_worker(fn, arg):
	def work():
		results = {}
		for y in range(get_world_size()):
			value = fn(arg)
			if value != None:
				results[(get_pos_x(), get_pos_y())] = value
			move(North)
		return results
	return work
	
def merge(into, part):
	for k in part:
		into[k] = part[k]
	
def sweep(fn, arg=None):
	n = get_world_size()
	goto(0, 0)
	work = column_worker(fn, arg)
	drones = []
	results = {}
	for x in range(n):
		d = spawn_drone(work)
		if d == None:
			merge(results, work())
		else:
			drones.append(d)
		move(East)
	for d in drones:
		merge(results, wait_for(d))
	return results