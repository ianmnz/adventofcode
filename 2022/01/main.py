# Advent of Code : Day 01 - Calorie Counting
# https://adventofcode.com/2022/day/1

import functools
from typing import List, Tuple

from helpers import Timer


@Timer.timeit
def sum_k_first_elements(array: List[int], k: int) -> int:
    return functools.reduce(lambda x, y: x + y, array[:k])


@Timer.timeit
def parse(filename: str) -> List[int]:
    with open(filename, "r") as file:
        inventory = [
            sum(map(int, items.split("\n")))
            for items in file.read().strip().split("\n\n")
        ]
    return inventory


@Timer.timeit
def solve(filename: str) -> Tuple[int, int]:
    inventory = parse(filename)
    inventory = sorted(inventory, reverse=True)
    part1 = sum_k_first_elements(inventory, 1)
    part2 = sum_k_first_elements(inventory, 3)

    return part1, part2


def main() -> None:
    import os

    res = solve(os.path.dirname(os.path.abspath(__file__)) + "/input.txt")

    assert res[0] == 71934, f"Part1 = {res[0]}"
    assert res[1] == 211447, f"Part2 = {res[1]}"


if __name__ == "__main__":
    main()
