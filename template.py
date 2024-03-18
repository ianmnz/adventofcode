# Advent of Code : Day DD - INSERT TITLE HERE
# https://adventofcode.com/yyyy/day/dd

from typing import List, Tuple

from helpers import Timer


@Timer.timeit
def parse(filename: str) -> List[str]:
    ...


@Timer.timeit
def solve(filename: str) -> Tuple[int, int]:
    _ = parse(filename)
    part1 = -1
    part2 = -1

    return part1, part2


def main() -> None:
    import os

    res = solve(os.path.dirname(os.path.abspath(__file__)) + "/input.txt")

    assert res[0] == -1, f"Part1 = {res[0]}"
    assert res[1] == -1, f"Part2 = {res[1]}"


if __name__ == "__main__":
    main()
