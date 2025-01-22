# Advent of Code : Day 03 - Gear Ratios
# https://adventofcode.com/2023/day/3

import math
import re

from helpers import Timer, load_input_data


@Timer.timeit
def sum_engine_parts_numbers(schematic: list[str]) -> int:
    n = len(schematic)
    m = len(schematic[0])

    symbols = {
        (i, j)
        for i in range(n)
        for j in range(m)
        if schematic[i][j] not in "0123456789."
    }
    engine = dict()

    for r, row in enumerate(schematic):
        for number in re.finditer(r"\d+", row):
            neighborhood = {
                (i, j)
                for i in (r - 1, r, r + 1)
                for j in range(number.start() - 1, number.end() + 1)
            }

            if symbols.intersection(neighborhood):
                engine[(r, number.start())] = int(number.group())

    return sum(engine.values())


@Timer.timeit
def sum_gear_ratios(schematic: list[str]) -> int:
    n = len(schematic)
    m = len(schematic[0])

    gears = {(i, j): [] for i in range(n) for j in range(m) if schematic[i][j] == "*"}

    for r, row in enumerate(schematic):
        for number in re.finditer(r"\d+", row):
            neighborhood = {
                (i, j)
                for i in (r - 1, r, r + 1)
                for j in range(number.start() - 1, number.end() + 1)
            }

            for gear in gears.keys() & neighborhood:  # intersection
                gears[gear].append(int(number.group()))

    return sum(math.prod(numbers) for numbers in gears.values() if len(numbers) == 2)


@Timer.timeit
def parse(data: str) -> list[str]:
    return data.split("\n")


@Timer.timeit
def solve(data: str) -> tuple[int, int]:
    schematic = parse(data)
    part1 = sum_engine_parts_numbers(schematic)
    part2 = sum_gear_ratios(schematic)

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2023, 3)))
