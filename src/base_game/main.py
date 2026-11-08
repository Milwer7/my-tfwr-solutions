import drone_config
import scheduler

drone_config.init()
clear()

while True:
	item = scheduler.resolve(scheduler.most_needed())
	scheduler.run_for(item)