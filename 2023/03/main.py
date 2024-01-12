# Advent of Code : Day 03 - Gear Ratios
# https://adventofcode.com/2023/day/3


import re
import math
from typing import List, Tuple


def sum_engine_parts_numbers(schematic: List[str]) -> int:
    n = len(schematic)
    m = len(schematic[0])

    symbols = {(i, j) for i in range(n) for j in range(m) if schematic[i][j] not in '0123456789.'}
    engine = dict()

    for r, row in enumerate(schematic):
        for number in re.finditer(f'\d+', row):
            neighborhood = {(i, j) for i in (r - 1, r, r + 1)
                                for j in range(number.start() - 1, number.end() + 1)}

            if symbols.intersection(neighborhood):
                engine[(r, number.start())] = int(number.group())

    return sum(engine.values())


def sum_gear_ratios(schematic: List[str]) -> int:
    n = len(schematic)
    m = len(schematic[0])

    gears = {(i, j): [] for i in range(n) for j in range(m) if schematic[i][j] == '*'}

    for r, row in enumerate(schematic):
        for number in re.finditer(f'\d+', row):
            neighborhood = {(i, j) for i in (r - 1, r, r + 1)
                                for j in range(number.start() - 1, number.end() + 1)}

            for gear in gears.keys() & neighborhood:    # intersection
                gears[gear].append(int(number.group()))

    return sum(math.prod(numbers) for numbers in gears.values() if len(numbers) == 2)


def solve(filename: str) -> Tuple[int, int]:
    with open(filename, "r") as file:
        schematic = file.read().split('\n')

    part1 = sum_engine_parts_numbers(schematic)
    part2 = sum_gear_ratios(schematic)

    return part1, part2


def main():
    import os
    from helpers import Timer

    with Timer():
        res = solve(os.path.dirname(os.path.abspath(__file__)) + "/input.txt")

        assert res[0] == 533775,   f"Part1 = {res[0]}"
        assert res[1] == 78236071, f"Part2 = {res[1]}"


if __name__ == "__main__":
    main()
