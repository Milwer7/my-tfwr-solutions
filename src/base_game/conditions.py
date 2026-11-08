def is_empty():
	return get_entity_type() == None

def is_entity(entity):
	return get_entity_type() == entity

def is_ground(ground):
	return get_ground_type() == ground

SOIL_CROPS = {
	Entities.Carrot: True,
	Entities.Pumpkin: True,
	Entities.Sunflower: True,
	Entities.Cactus: True,
}
FERTILIZE = {Entities.Pumpkin: True, Entities.Tree: True, Entities.Sunflower: True}

def needs_soil(entity):
	return entity in SOIL_CROPS
	
def needs_grassland(entity):
	return entity == Entities.Grass

def is_wrong_crop(entity):
	return not is_empty() and not is_entity(entity)
	
def is_pumpkin_ready():
	return is_entity(Entities.Pumpkin) and can_harvest()
	
def wants_water(entity):
	return entity != Entities.Grass
	
def wants_fertilizer(entity):
	return entity in FERTILIZE
		
POLY_CROPS = {Entities.Grass: True, Entities.Bush: True, Entities.Tree: True, Entities.Carrot: True}
PROTECTED = {Entities.Pumpkin: True, Entities.Sunflower: True, Entities.Cactus: True}

def is_poly(entity):
	return entity in POLY_CROPS