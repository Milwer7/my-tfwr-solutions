import actions
import board
import conditions
import nav

def make_plan(focus):
	n = get_world_size()
	plan = board.make_board(n)
	for x in range(n):
		for y in range(n):
			if focus == Entities.Tree:
				if (x + y) % 2 == 0:
					plan[x][y] = Entities.Tree
				else:
					plan[x][y] = Entities.Bush
			else:
				plan[x][y] = focus
	return plan

def tend_tile(state):
	pos = (get_pos_x(), get_pos_y())
	entity = state["plan"][pos[0]][pos[1]]
	if pos in state["overrides"]:
		entity = state["overrides"][pos]
	actions.tend(entity)
	if conditions.is_poly(entity):
		return actions.companion_request(state["plan"])
	return None

def run(focus, passes=3):
	state = {"plan": make_plan(focus), "overrides": {}}
	for i in range(passes):
		requests = nav.sweep(tend_tile, state)
		overrides = {}
		for tile in requests:
			req = requests[tile]
			overrides[req[1]] = req[0]
		state["overrides"] = overrides