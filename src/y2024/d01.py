# Advent of Code : Day 01 - Historian Hysteria
# https://adventofcode.com/2024/day/01

import os
from collections import Counter

from helpers import Timer


@Timer.timeit
def get_total_distance(l_ids: list[int], r_ids: list[int]) -> int:
    return sum(abs(lhs - rhs) for lhs, rhs in zip(sorted(l_ids), sorted(r_ids)))


@Timer.timeit
def get_similarity_score(l_ids: list[int], r_ids: list[int]) -> int:
    counter = Counter(r_ids)
    return sum(lhs * counter[lhs] for lhs in l_ids if lhs in counter)


@Timer.timeit
def parse(filename: os.PathLike) -> tuple[list[int], list[int]]:
    with open(filename, "r") as file:
        locations = [tuple(map(int, x.split())) for x in file.read().splitlines()]

    l_ids = [loc[0] for loc in locations]
    r_ids = [loc[1] for loc in locations]

    return l_ids, r_ids


@Timer.timeit
def solve(filename: os.PathLike) -> tuple[int, int]:
    l_ids, r_ids = parse(filename)
    part1 = get_total_distance(l_ids, r_ids)
    part2 = get_similarity_score(l_ids, r_ids)

    return part1, part2
