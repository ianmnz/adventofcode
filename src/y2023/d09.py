# Advent of Code : Day 09 - Mirage Maintenance
# https://adventofcode.com/2023/day/9

import os

from helpers import Timer


def extrapolate(history: list[int]) -> int:
    deltas = [t - t_1 for t_1, t in zip(history, history[1:])]
    return history[-1] + extrapolate(deltas) if any(t != 0 for t in history) else 0


@Timer.timeit
def parse(filename: os.PathLike) -> list[list[int]]:
    with open(filename, "r") as file:
        histories = [[*map(int, line.split())] for line in file]
    return histories


@Timer.timeit
def solve(filename: os.PathLike) -> tuple[int, int]:
    histories = parse(filename)
    part1 = sum([extrapolate(history) for history in histories])
    part2 = sum([extrapolate(history[::-1]) for history in histories])

    return part1, part2
