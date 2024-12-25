# Advent of Code : Day 25 - Code Chronicle
# https://adventofcode.com/2024/day/25

from helpers import Timer, load_input_data

N = 5


@Timer.timeit
def check_lock_key_pair_fit(locks: list[set[str]], keys: list[set[str]]) -> int:
    return sum(not (lock & key) for lock in locks for key in keys)


@Timer.timeit
def parse(data: str) -> tuple[list[set[str]], list[set[str]]]:
    locks, keys = [], []

    for schematic in data.split("\n\n"):
        pattern = {i for i, char in enumerate(schematic) if char == "#"}

        if schematic[0] == "#":
            locks.append(pattern)
        else:
            keys.append(pattern)

    return locks, keys


@Timer.timeit
def solve(data: str) -> int:
    locks, keys = parse(data)
    part1 = check_lock_key_pair_fit(locks, keys)

    return part1


if __name__ == "__main__":
    print(solve(load_input_data(2024, 25)))
