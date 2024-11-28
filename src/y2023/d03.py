# Advent of Code : Day 03 - Gear Ratios
# https://adventofcode.com/2023/day/3

import math
import os
import re

from helpers import Timer


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
def parse(filename: os.PathLike) -> list[str]:
    with open(filename, "r") as file:
        schematic = file.read().split("\n")
    return schematic


@Timer.timeit
def solve(filename: os.PathLike) -> tuple[int, int]:
    schematic = parse(filename)
    part1 = sum_engine_parts_numbers(schematic)
    part2 = sum_gear_ratios(schematic)

    return part1, part2
