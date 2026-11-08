# The Farmer Was Replaced — My Solutions

My scripts for [The Farmer Was Replaced](https://store.steampowered.com/app/2060160/The_Farmer_Was_Replaced/), a programming game where you automate a farm with a drone using a Python-like language.

The entry point is `main.py`: a scheduler that keeps every resource stocked by picking whatever the farm needs most and running the right routine for it, forever.

> ⚠️ **`main.py` calls `clear()` on start**, which wipes the current farm.

## Requirements

The main loop assumes **everything in the base game is unlocked**: Megafarm (multiple drones), polyculture, all crops, mazes, dinosaurs, fertilizer, water, and so on. Individual modules may work with fewer unlocks, but that's not tested.

The Miner Was Replaced DLC is **not** covered yet.

## Installation

The game stores each code window as a `.py` file in your save folder:

```
Windows: %USERPROFILE%\AppData\LocalLow\TheFarmerWasReplaced\TheFarmerWasReplaced\Saves\Save0\
Linux (Proton): steamapps/compatdata/2060160/pfx/drive_c/users/steamuser/AppData/LocalLow/TheFarmerWasReplaced/TheFarmerWasReplaced/Saves/Save0/
```

Copy the files from `base_game/` into that folder (or into a different `SaveN` slot) and run `main` in the game. **Keep the filenames unchanged**, because the modules import each other by name.

These files only run inside the game. Running them with regular Python won't do anything useful.

## Structure

| File | Role |
|---|---|
| `main.py` | Entry point: init, clear the farm, loop the scheduler |
| `scheduler.py` | Picks the most-needed resource and dispatches the matching farm |
| `nav.py` | Movement and the parallel `sweep` used by most farms |
| `actions.py` | Per-tile actions: tilling, planting, watering, fertilizing, companions |
| `conditions.py` | Crop rules and tile checks |
| `board.py` | 2D board helpers for layouts |
| `crops.py` | Grass, trees/bushes and carrots with polyculture |
| `pumpkins.py` | Giant pumpkin farm |
| `sunflowers.py` | Power farm |
| `cactus.py` | Cactus sorting farm |
| `maze.py` | Gold (treasure maze) solver |
| `dinosaur.py` | Bones (snake) farm |
| `drone_config.py` | Drone appearance (hat) |

## Algorithms

### Scheduler (`scheduler.py`)
- Every resource has a target amount. Each round, the scheduler picks the resource with the **lowest current/target ratio**.
- **Recursive dependency resolution:** before farming a crop, it checks `get_cost()` for a full field of it. If an ingredient is short, it farms that ingredient first (up to 3 levels deep).
- Gold only runs when there's enough Weird Substance for a maze, and bones only when Dinosaurs are unlocked.

### Navigation and parallelism (`nav.py`)
- **Wrap-around shortest path:** the farm is a torus, so each axis moves whichever way is shorter.
- **Parallel sweep:** one drone per column runs a per-tile function, returns a `{(x, y): value}` dict, and the results are merged with `wait_for()`. If no drone can be spawned, the main drone does that column itself.

### Polyculture (`crops.py`, `actions.py`)
- Builds a planting plan for the whole field (a tree/bush checkerboard for wood, so trees don't grow next to each other).
- After each pass, it reads every plant's companion request (`get_companion()`) and applies them as overrides on the next pass. Pumpkins, sunflowers and cacti are protected and are never overridden.

### Pumpkins (`pumpkins.py`)
- Keeps sweeping and replanting dead pumpkins until every tile holds a ready pumpkin, so they merge into a giant pumpkin. Then it harvests once. A pass limit prevents infinite loops.

### Sunflowers (`sunflowers.py`)
- Plants the field and records each sunflower's petal count. Then it greedily harvests the **sunflower with the most petals** each time, to get the power bonus. It stops below 10 sunflowers, where the bonus no longer applies.

### Cactus (`cactus.py`)
- Sorts the field with a **parallel bubble sort**: one drone per row sorts along the row, then one drone per column sorts along the column.
- Each line uses early exit (stops once a pass makes no swap) and shrinks its range, because the largest value settles at the end after each pass.
- Once the field is sorted, a single harvest collects all of it.

### Maze (`maze.py`)
- **Parallel mapping:** the field is split into column strips, one drone per strip. Each drone runs a DFS that records every cell's walls. Strips overlap by a margin, so paths that briefly leave a strip still get mapped.
- **A\*** with a hand-written binary heap (lazy deletion of stale entries), Manhattan heuristic, and tie-breaking toward deeper nodes.
- **Optimistic planning:** unknown cells are assumed open, and the drone replans when it hits a wall.
- **Treasure reuse:** the maze is reused while Weird Substance lasts. Reuse can remove walls, so the map is refreshed on every visited cell and the paths keep getting shorter.

### Dinosaur (`dinosaur.py`)
- Builds a **Hamiltonian cycle**: columns zigzag over rows 1..n-1 and row 0 is the return lane. Following the cycle can never trap the snake.
- **Safe shortcuts:** while the snake is under half the field, it may skip forward along the cycle toward the apple. It never jumps past the apple and never gets close to its own tail.
- It stops after a full lap without eating, then removes the hat to turn the tail into bones.

## Deprecated / unused code

Some code isn't used by the main loop anymore. I kept it because it shows how the solutions evolved, or because it's useful in other setups.

- **`cactus.py`: `plant_region`, `sort_region`, `wait_grown`, `run_region`.** The original single-drone cactus farm, which sorts a square region with one drone. It was replaced by the row/column parallel version once I had Megafarm. It's still useful without extra drones or for testing on a small region.
- **`board.py`: `fill_rows`, `fill_columns`, `fill_checker`, `fill_from`, `positions_of`.** Layout helpers from when I was experimenting with polyculture patterns. `crops.py` now builds its own plan and only uses `make_board`.

## How this code was made

Roughly **70% written by me and 30% AI-assisted** (Claude). The AI parts were mostly reviews, bug-finding and planning stuff. For example, the maze's map gave me headaches because I refused to make a simple embrace the right wall approach hahaha. Everything was tested and adjusted in the game (November 7th, 2026)

## About the game

This game is a lot of fun. It starts with moving a drone one tile at a time and somehow ends with A* in a hedge maze, parallel sorting algorithms on cacti, and a snake that follows a Hamiltonian cycle. Every unlock gives you a new problem that is really an algorithms problem in disguise. Watching a few dozen drones farm in parallel with code you wrote is very satisfying.

If you like programming, I recommend it.

## License

I always forget the licensing stuff but you are able to use this code however you like, credits are always appreciated tho.
