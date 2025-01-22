# Advent of Code : Day 04 - Camp Cleanup
# https://adventofcode.com/2022/day/4

import re
from typing import NamedTuple

from helpers import Timer, load_input_data


class Range(NamedTuple):
    lower: int
    upper: int


@Timer.timeit
def parse(data: str) -> list[tuple[Range, Range]]:
    pattern = re.compile(r"(\d+)-(\d+),(\d+)-(\d+)")
    matches = [pattern.match(line) for line in data.strip().split("\n")]

    return [
        (
            Range(int(match.group(1)), int(match.group(2))),
            Range(int(match.group(3)), int(match.group(4))),
        )
        for match in matches
        if match is not None
    ]


@Timer.timeit
def find_nb_intersections(ranges: list[tuple[Range, Range]]) -> tuple[int, int]:
    nb_fully_contained = 0
    nb_overlapped_not_fully_contained = 0

    for left, right in ranges:
        if ((left.lower <= right.lower) and (right.upper <= left.upper)) or (
            (right.lower <= left.lower) and (left.upper <= right.upper)
        ):
            nb_fully_contained += 1

        elif (left.lower <= right.lower <= left.upper) or (
            right.lower <= left.lower <= right.upper
        ):
            nb_overlapped_not_fully_contained += 1

    return nb_fully_contained, nb_overlapped_not_fully_contained


@Timer.timeit
def solve(data: str) -> tuple[int, int]:
    ranges = parse(data)
    (
        nb_fully_contained,
        nb_overlapped_not_fully_contained,
    ) = find_nb_intersections(ranges)

    part1 = nb_fully_contained
    part2 = nb_fully_contained + nb_overlapped_not_fully_contained

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2022, 4)))
