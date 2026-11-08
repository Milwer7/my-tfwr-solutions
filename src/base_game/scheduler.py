import crops
import pumpkins
import sunflowers
import cactus
import maze
import dinosaur

TARGETS = {
	Items.Hay: 5000,
	Items.Wood: 5000,
	Items.Carrot: 3000,
	Items.Pumpkin: 3000,
	Items.Power: 1000,
	Items.Cactus: 2000,
	Items.Gold: 1000,
	Items.Bone: 1000,
}

SOURCE = {
	Items.Hay: Entities.Grass,
	Items.Wood: Entities.Tree,
	Items.Carrot: Entities.Carrot,
	Items.Pumpkin: Entities.Pumpkin,
	Items.Power: Entities.Sunflower,
	Items.Cactus: Entities.Cactus,
}

def most_needed():
	best = None
	best_ratio = 0
	for item in TARGETS:
		if item == Items.Gold and num_items(Items.Weird_Substance) < maze.cost():
			continue
		if item == Items.Bone and num_unlocked(Unlocks.Dinosaurs) == 0:
			continue
		ratio = num_items(item) / TARGETS[item]
		if best == None or ratio < best_ratio:
			best = item
			best_ratio = ratio
	return best

def resolve(item, depth=0):
	# if we can't afford a full farm of this crop, farm the missing ingredient
	if not (item in SOURCE) or depth > 3:
		return item
	cost = get_cost(SOURCE[item])
	n = get_world_size()
	for c in cost:
		if num_items(c) < cost[c] * n * n:
			if c in SOURCE:
				return resolve(c, depth + 1)
			return item
	return item

def run_for(item):
	if item == Items.Hay:
		crops.run(Entities.Grass)
	elif item == Items.Wood:
		crops.run(Entities.Tree)
	elif item == Items.Carrot:
		crops.run(Entities.Carrot)
	elif item == Items.Pumpkin:
		pumpkins.run()
	elif item == Items.Power:
		sunflowers.run()
	elif item == Items.Cactus:
		cactus.run()
	elif item == Items.Gold:
		maze.run()
	elif item == Items.Bone:
		dinosaur.run()