# Advent of Code : Day 01 - Calorie Counting
# https://adventofcode.com/2022/day/1

import functools
import os

from helpers import Timer


@Timer.timeit
def sum_k_first_elements(array: list[int], k: int) -> int:
    return functools.reduce(lambda x, y: x + y, array[:k])


@Timer.timeit
def parse(filename: os.PathLike) -> list[int]:
    with open(filename, "r") as file:
        inventory = [
            sum(map(int, items.split("\n")))
            for items in file.read().strip().split("\n\n")
        ]
    return inventory


@Timer.timeit
def solve(filename: os.PathLike) -> tuple[int, int]:
    inventory = parse(filename)
    inventory = sorted(inventory, reverse=True)
    part1 = sum_k_first_elements(inventory, 1)
    part2 = sum_k_first_elements(inventory, 3)

    return part1, part2
