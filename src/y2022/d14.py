# Advent of Code : Day 14 - Regolith Reservoir
# https://adventofcode.com/2022/day/14


from helpers import Timer, load_input_data

Coordinate = tuple[int, int]
Scanner = set[Coordinate]

BOTTOM = 0


@Timer.timeit
def scan(cave: list[list[str]]) -> Scanner:
    scanner: Scanner = set()

    global BOTTOM

    for walls in cave:
        for curr, next in zip(walls[:-1], walls[1:]):
            curr_x, curr_y = map(int, curr.split(","))
            next_x, next_y = map(int, next.split(","))

            lower_x, upper_x = sorted((curr_x, next_x))
            lower_y, upper_y = sorted((curr_y, next_y))

            for x in range(lower_x, upper_x + 1):
                for y in range(lower_y, upper_y + 1):
                    scanner.add((x, y))  # Rocks
                    BOTTOM = max(BOTTOM, y)

    BOTTOM += 2
    return scanner


def simulate_sand_fall(scanner: Scanner, source: Coordinate) -> Coordinate:
    curr_x, curr_y = source

    while True:
        if curr_y + 1 >= BOTTOM:
            break  # Reached bottom

        if (curr_x, curr_y + 1) not in scanner:
            curr_y += 1

        elif (curr_x - 1, curr_y + 1) not in scanner:
            curr_x -= 1
            curr_y += 1

        elif (curr_x + 1, curr_y + 1) not in scanner:
            curr_x += 1
            curr_y += 1

        else:
            break  # Sand came to rest

    scanner.add((curr_x, curr_y))
    return (curr_x, curr_y)


@Timer.timeit
def simulate_up_to_reaching_bottom(
    scanner: Scanner, source: Coordinate = (500, 0)
) -> int:
    nb_sand_units_that_came_to_rest = 0
    while sand := simulate_sand_fall(scanner, source):
        if sand[1] + 1 >= BOTTOM:
            break

        nb_sand_units_that_came_to_rest += 1
    return nb_sand_units_that_came_to_rest


@Timer.timeit
def simulate_up_to_blocking_source(
    scanner: Scanner, source: Coordinate = (500, 0)
) -> int:
    nb_sand_units_that_came_to_rest = 0
    while sand := simulate_sand_fall(scanner, source):
        nb_sand_units_that_came_to_rest += 1

        if sand == source:
            break

    return nb_sand_units_that_came_to_rest


@Timer.timeit
def parse(data: str) -> list[list[str]]:
    return [line.strip().split(" -> ") for line in data.strip().split("\n")]


@Timer.timeit
def solve(data: str) -> Coordinate:
    cave = parse(data)
    scanner = scan(cave)
    part1 = simulate_up_to_reaching_bottom(scanner)
    # For performance purposes, i.e., avoid redoing the first part
    # we just complete the simulation with a +1 factor of correction
    part2 = (part1 + 1) + simulate_up_to_blocking_source(scanner)

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2022, 14)))
