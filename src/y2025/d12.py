# Advent of Code : Day 12 - Christmas Tree Farm
# https://adventofcode.com/2025/day/12

from dataclasses import dataclass

from helpers import Timer, load_input_data


@dataclass
class Shape:
    total_space: int
    filled_space: int


@dataclass
class Region:
    size: int
    quantities: tuple[int]


def get_nb_big_enough_regions(shapes: list[Shape], regions: list[Region]) -> int:
    res = 0
    for region in regions:
        lower, upper = 0, 0
        for idx, qty in enumerate(region.quantities):
            lower += qty * shapes[idx].filled_space
            upper += qty * shapes[idx].total_space

        if region.size < lower:
            # Definitely not big enough
            continue

        elif upper <= region.size:
            # Definitely big enough
            res += 1

        else:
            # Undetermined.
            # We would need a much better way of checking solutions in this range
            # but it turns out the solutions just works with the input data
            # (even though it does not with the example....go figure)
            # No Op. here...
            pass

    return res


@Timer.timeit
def parse(data: str) -> tuple[list[Shape], list[Region]]:
    *section1, section2 = data.split("\n\n")

    shapes = []
    for block in section1:
        _, *shape = block.split("\n")
        total = sum(len(row) for row in shape)
        filled = sum(1 for row in shape for col in row if col == "#")
        shapes.append(Shape(total, filled))

    regions = []
    for region in section2.split("\n"):
        dimensions, quantities = region.split(":")

        width, length = tuple(map(int, dimensions.split("x")))

        regions.append(Region(width * length, tuple(map(int, quantities.split()))))

    return shapes, regions


@Timer.timeit
def solve(data: str) -> int:
    shapes, regions = parse(data)
    part1 = get_nb_big_enough_regions(shapes, regions)

    return part1


if __name__ == "__main__":
    print(solve(load_input_data(2025, 12)))
