# Advent of Code : Day 13 - Point of Incidence
# https://adventofcode.com/2023/day/13


from typing import List, Tuple

from helpers import Timer


def transpose(pattern: List[str]) -> List[str]:
    return [
        [pattern[j][i] for j in range(len(pattern))] for i in range(len(pattern[0]))
    ]


def find_reflection_point(pattern: List[str], expected_smudges: int) -> int:
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
def summarize_patterns(patterns: List[List[str]], expected_smudges: int) -> int:
    ans = 0
    for pattern in patterns:
        # Horizontal symmetry
        ans += 100 * find_reflection_point(pattern, expected_smudges)
        # Vertical symmetry
        ans += 1 * find_reflection_point(transpose(pattern), expected_smudges)
    return ans


@Timer.timeit
def parse(filename: str) -> List[List[str]]:
    with open(filename, "r") as file:
        patterns = [line.split("\n") for line in file.read().split("\n\n")]
    return patterns


@Timer.timeit
def solve(filename: str) -> Tuple[int, int]:
    patterns = parse(filename)
    part1 = summarize_patterns(patterns, 0)
    part2 = summarize_patterns(patterns, 1)

    return part1, part2


def main():
    import os

    res = solve(os.path.dirname(os.path.abspath(__file__)) + "/input.txt")

    assert res[0] == 34772, f"Part1 = {res[0]}"
    assert res[1] == 35554, f"Part2 = {res[1]}"


if __name__ == "__main__":
    main()
