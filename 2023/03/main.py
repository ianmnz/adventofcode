# Advent of Code : Day 03 - Gear Ratios
# https://adventofcode.com/2023/day/3


import re
import math
from typing import List


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


def main():
    import os
    import sys

    # To be able to import the helpers module
    sys.path.append(os.path.dirname(                                        # Project
                        os.path.dirname(                                    # Year
                            os.path.dirname(os.path.abspath(__file__)))))   # Day

    from helpers import Timer

    with open("input.txt", "r") as file:
        schematic = file.read().split('\n')

    # --- Part 1 --- #
    with Timer():
        print("The sum of the engine parts is:", sum_engine_parts_numbers(schematic))  # 533775

    # --- Part 2 --- #
    with Timer():
        print("The sum of the gear ratios is:", sum_gear_ratios(schematic))  # 78236071


if __name__ == "__main__":
    main()
