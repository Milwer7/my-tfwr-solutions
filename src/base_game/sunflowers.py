import actions
import conditions
import nav

MIN_SUNFLOWERS = 10

def tend_tile(arg):
	actions.tend(Entities.Sunflower, False)
	if conditions.is_entity(Entities.Sunflower):
		return measure()
	return None

def find_max(petals):
	best = None
	best_p = -1
	for pos in petals:
		if petals[pos] > best_p:
			best_p = petals[pos]
			best = pos
	return best

def run():
	petals = nav.sweep(tend_tile)
	while len(petals) >= MIN_SUNFLOWERS:
		pos = find_max(petals)
		nav.goto(pos[0], pos[1])
		while not can_harvest():
			pass
		harvest()
		petals.pop(pos)