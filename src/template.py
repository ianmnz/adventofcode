# Advent of Code : Day DD - INSERT TITLE HERE
# https://adventofcode.com/yyyy/day/dd

import os

from helpers import Timer


@Timer.timeit
def parse(filename: os.PathLike) -> list[str]:
    ...


@Timer.timeit
def solve(filename: os.PathLike) -> tuple[int, int]:
    _ = parse(filename)
    part1 = -1
    part2 = -1

    return part1, part2


def test_day_XX(data_dir):
    # from src.y202X.dXX import solve

    res1, res2 = solve(data_dir / "202XXX.txt")

    assert res1 == -1, f"Part1 = {res1}"
    assert res2 == -1, f"Part2 = {res2}"


def main() -> None:
    from pathlib import Path

    res = solve(Path(__file__).parent / "input.txt")

    assert res[0] == -1, f"Part1 = {res[0]}"
    assert res[1] == -1, f"Part2 = {res[1]}"


if __name__ == "__main__":
    main()