# Advent of Code : Day 13 - Point of Incidence
# https://adventofcode.com/2023/day/13

import os

from helpers import Timer


def transpose(pattern: list[str]) -> list[list[str]]:
    return [
        [pattern[j][i] for j in range(len(pattern))] for i in range(len(pattern[0]))
    ]


def find_reflection_point(pattern: list[str], expected_smudges: int) -> int:
    def check_reflection_point(pattern_l: str, pattern_r: str) -> bool:
        diffs = 0
        for row_l, row_r in zip(pattern_l, pattern_r):
            for l, r in zip(row_l, row_r):
                diffs += int(l != r)

                if diffs > expected_smudges:
                    return False

        return diffs == expected_smudges

    for reflection in range(1, len(pattern)):
        if check_reflection_point(pattern[reflection - 1 :: -1], pattern[reflection:]):
            return reflection

    return 0


@Timer.timeit
def summarize_patterns(patterns: list[list[str]], expected_smudges: int) -> int:
    ans = 0
    for pattern in patterns:
        # Horizontal symmetry
        ans += 100 * find_reflection_point(pattern, expected_smudges)
        # Vertical symmetry
        ans += 1 * find_reflection_point(transpose(pattern), expected_smudges)
    return ans


@Timer.timeit
def parse(filename: os.PathLike) -> list[list[str]]:
    with open(filename, "r") as file:
        patterns = [line.split("\n") for line in file.read().split("\n\n")]
    return patterns


@Timer.timeit
def solve(filename: os.PathLike) -> tuple[int, int]:
    patterns = parse(filename)
    part1 = summarize_patterns(patterns, 0)
    part2 = summarize_patterns(patterns, 1)

    return part1, part2
