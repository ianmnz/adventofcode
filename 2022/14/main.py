# Advent of Code : Day 14 - Regolith Reservoir
# https://adventofcode.com/2022/day/14

# RE-DO BECAUSE UGLY

import numpy as np

WALL = 8
EMPTY = 1
SAND = 2
SOURCE = 0


def draw(interval_x: tuple, interval_y: tuple, source: tuple, walls: list) -> np.array:
    min_x, max_x = interval_x
    min_y, max_y = interval_y

    grid = EMPTY * np.ones((max_y - min_y + 3, max_x - min_x + 3), dtype=int)

    source_x, source_y = source

    source_x -= min_x - 1
    source_y -= min_y

    grid[source_y, source_x] = SOURCE

    for wall in walls:
        curr_x, curr_y = wall[0]

        curr_x -= min_x - 1
        curr_y -= min_y - 1

        grid[curr_y, curr_x] = WALL
        for idx in range(1, len(wall)):
            next_x, next_y = wall[idx]

            next_x -= min_x - 1
            next_y -= min_y - 1

            grid[next_y, next_x] = WALL

            if curr_y == next_y: # Vertical line
                for i in range(min(curr_x, next_x) + 1, max(curr_x, next_x)):
                    grid[curr_y, i] = WALL

            elif curr_x == next_x: # Horizontal line
                for j in range(min(curr_y, next_y) + 1, max(curr_y, next_y)):
                    grid[j, curr_x] = WALL

            curr_x, curr_y = next_x, next_y

    return grid


def main():
    source = (500, 0)
    min_x = 10000
    max_x = -10000
    min_y = 0 # We add the source to the grid
    max_y = -10000

    walls = []

    with open('input.txt', 'r') as file:
        for line in file:
            line = line.strip().split(' -> ')

            wall = []
            for pair in line:
                x, y = [int(val) for val in pair.split(',')]

                wall.append((x, y))

                if x < min_x:
                    min_x = x

                if x > max_x:
                    max_x = x

                if y < min_y:
                    min_y = y

                if y > max_y:
                    max_y = y

            walls.append(wall)
    # print(min_x, max_x, min_y, max_y)

    # --- For part2 ---
    max_y += 2
    max_x += max_y
    min_x -= max_y
    walls.append([(min_x - 1, max_y), (max_x + 1, max_y)])
    # --- ---

    grid = draw((min_x, max_x), (min_y, max_y), source, walls)
    # print(grid)

    found = False
    nb_sand_units_that_rest = 0
    while not found:
        sand_x, sand_y = source

        sand_x -= min_x - 1
        sand_y -= min_y - 1

        while True:
            if not (0 <= sand_y < (max_y - min_y + 3) - 1):
               found = True
               break

            if grid[sand_y + 1, sand_x] == EMPTY:
                sand_y += 1
            elif grid[sand_y + 1, sand_x - 1] == EMPTY:
                sand_x -= 1
                sand_y += 1
            elif grid[sand_y + 1, sand_x + 1] == EMPTY:
                sand_x += 1
                sand_y += 1
            else:
                nb_sand_units_that_rest += 1
                grid[sand_y, sand_x] = SAND
                # print(nb_sand_units_that_rest)
                # print(grid)
                if sand_y == 1:
                    found = True
                break

    # Answer part 1 :
    print(f"Number of units of sand that come "
        f"to rest before falling eternally: {nb_sand_units_that_rest}") # 843

    # Answer part 2 :
    print(f"Number of units of sand that come "
        f"to rest before blocking the source: {nb_sand_units_that_rest}") # 27625

if __name__ == "__main__":
    main()