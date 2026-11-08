import conditions

def ensure_ground(ground):
	if not conditions.is_ground(ground):
		till()

def water(threshold=0.75):
	if get_water() < threshold and num_items(Items.Water) > 0:
		use_item(Items.Water)

def clear_tile(entity, allow_harvest=True):
	if conditions.is_wrong_crop(entity):
		harvest()
	elif allow_harvest and can_harvest():
		harvest()

def tend(entity, allow_harvest=True):
	clear_tile(entity, allow_harvest)
	if conditions.needs_soil(entity):
		ensure_ground(Grounds.Soil)
	elif conditions.needs_grassland(entity):
		ensure_ground(Grounds.Grassland)
	if not conditions.is_entity(entity):
		plant(entity)
	if conditions.wants_water(entity):
		water()
	fertilize(entity)
			
def fertilize(entity):
	if not conditions.wants_fertilizer(entity):
		return
	if can_harvest():
		return
	if num_items(Items.Fertilizer) > 0:
		use_item(Items.Fertilizer)
		
def companion_request(plan):
	companion = get_companion()
	if companion == None:
		return None
	pos = companion[1]
	if plan[pos[0]][pos[1]] in conditions.PROTECTED:
		return None
	return companion