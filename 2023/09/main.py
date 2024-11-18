# Advent of Code : Day 09 - Mirage Maintenance
# https://adventofcode.com/2023/day/9

import os
from typing import List, Tuple

from helpers import Timer


def extrapolate(history: List[int]) -> int:
    deltas = [t - t_1 for t_1, t in zip(history, history[1:])]
    return history[-1] + extrapolate(deltas) if any(t != 0 for t in history) else 0


@Timer.timeit
def parse(filename: os.PathLike) -> List[List[int]]:
    with open(filename, "r") as file:
        histories = [[*map(int, line.split())] for line in file]
    return histories


@Timer.timeit
def solve(filename: os.PathLike) -> Tuple[int, int]:
    histories = parse(filename)
    part1 = sum([extrapolate(history) for history in histories])
    part2 = sum([extrapolate(history[::-1]) for history in histories])

    return part1, part2


def main():
    from pathlib import Path

    res = solve(Path(__file__).parent / "input.txt")

    assert res[0] == 1939607039, f"Part1 = {res[0]}"
    assert res[1] == 1041, f"Part2 = {res[1]}"


if __name__ == "__main__":
    main()
