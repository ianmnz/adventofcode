# Advent of Code : Day DD - INSERT TITLE HERE
# https://adventofcode.com/yyyy/day/dd

import os
from typing import List, Tuple

from helpers import Timer


@Timer.timeit
def parse(filename: os.PathLike) -> List[str]:
    ...


@Timer.timeit
def solve(filename: os.PathLike) -> Tuple[int, int]:
    _ = parse(filename)
    part1 = -1
    part2 = -1

    return part1, part2


def main() -> None:
    from pathlib import Path

    res = solve(Path(__file__).parent / "input.txt")

    assert res[0] == -1, f"Part1 = {res[0]}"
    assert res[1] == -1, f"Part2 = {res[1]}"


if __name__ == "__main__":
    main()
