# Advent of Code : Day 01 - Calorie Counting
# https://adventofcode.com/2022/day/1

import functools

from helpers import Timer, load_input_data


@Timer.timeit
def sum_k_first_elements(array: list[int], k: int) -> int:
    return functools.reduce(lambda x, y: x + y, array[:k])


@Timer.timeit
def parse(data: str) -> list[int]:
    return [sum(map(int, items.split("\n"))) for items in data.strip().split("\n\n")]


@Timer.timeit
def solve(data: str) -> tuple[int, int]:
    inventory = parse(data)
    inventory = sorted(inventory, reverse=True)
    part1 = sum_k_first_elements(inventory, 1)
    part2 = sum_k_first_elements(inventory, 3)

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2022, 1)))
