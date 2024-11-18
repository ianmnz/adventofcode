# Advent of Code : Day 18 - Lavaduct Lagoon
# https://adventofcode.com/2023/day/18

import os
from typing import List, Tuple

from helpers import Timer

direction = {
    "R": (0, 1),
    "0": (0, 1),
    "D": (1, 0),
    "1": (1, 0),
    "L": (0, -1),
    "2": (0, -1),
    "U": (-1, 0),
    "3": (-1, 0),
}


@Timer.timeit
def dig(plan: List[List[str]], is_color_code: bool = False) -> int:
    def parse(command: List[str]) -> Tuple[int]:
        dir, length, color = command

        if not is_color_code:
            return *direction[dir], int(length)
        else:
            return *direction[color[7]], int(color[2:7], 16)

    row, col, area = 0, 0, 0
    for command in plan:
        dx, dy, length = parse(command)

        row += length * dx
        col += length * dy

        # internal area + half perimeter
        area += (col * dx * length) + (length / 2)

    return int(area + 1)


@Timer.timeit
def parse(filename: os.PathLike) -> List[List[str]]:
    with open(filename, "r") as file:
        plan = [line.split() for line in file.read().split("\n")]
    return plan


@Timer.timeit
def solve(filename: os.PathLike) -> Tuple[int, int]:
    plan = parse(filename)
    part1 = dig(plan)
    part2 = dig(plan, True)

    return part1, part2


def main():
    from pathlib import Path

    res = solve(Path(__file__).parent / "input.txt")

    assert res[0] == 50603, f"Part1 = {res[0]}"
    assert res[1] == 96556251590677, f"Part2 = {res[1]}"


if __name__ == "__main__":
    main()
