# Advent of Code : Day 18 - Lavaduct Lagoon
# https://adventofcode.com/2023/day/18


from helpers import Timer, load_input_data

direction = {
    "R": (0, 1),
    "0": (0, 1),
    "D": (1, 0),
    "1": (1, 0),
    "L": (0, -1),
    "2": (0, -1),
    "U": (-1, 0),
    "3": (-1, 0),
}


@Timer.timeit
def dig(plan: list[list[str]], is_color_code: bool = False) -> int:
    def parse(command: list[str]) -> tuple[int, int, int]:
        dir, length, color = command

        if not is_color_code:
            return *direction[dir], int(length)
        else:
            return *direction[color[7]], int(color[2:7], 16)

    row, col, area = 0, 0, 0
    for command in plan:
        dx, dy, length = parse(command)

        row += length * dx
        col += length * dy

        # internal area + half perimeter
        area += (col * dx * length) + (length / 2)

    return int(area + 1)


@Timer.timeit
def parse(data: str) -> list[list[str]]:
    return [line.split() for line in data.split("\n")]


@Timer.timeit
def solve(data: str) -> tuple[int, int]:
    plan = parse(data)
    part1 = dig(plan)
    part2 = dig(plan, True)

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2023, 18)))
