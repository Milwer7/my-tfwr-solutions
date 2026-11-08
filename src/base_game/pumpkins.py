import actions
import conditions
import nav

def tend_tile(arg):
	actions.tend(Entities.Pumpkin, False)
	if conditions.is_pumpkin_ready():
		return True
	return None

def run(max_passes=20):
	n = get_world_size()
	passes = 0
	while len(nav.sweep(tend_tile)) < n * n and passes < max_passes:
		passes += 1
	harvest()