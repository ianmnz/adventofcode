# Advent of Code : Day 13 - Point of Incidence
# https://adventofcode.com/2023/day/13


from typing import List


def transpose(pattern: List[str]) -> List[str]:
    pattern_t = ['' for _ in range(len(pattern[0]))]
    for row in pattern:
        for j, col in enumerate(row):
            pattern_t[j] += col
    return pattern_t


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
        if check_reflection_point(pattern[reflection - 1::-1], pattern[reflection:]):
            return reflection

    return 0


def summarize_patterns(patterns: List[List[str]], expected_smudges: int) -> int:
    ans = 0
    for pattern in patterns:
        ans += 100 * find_reflection_point(pattern, expected_smudges)             # Horizontal symmetry
        ans += 1 * find_reflection_point(transpose(pattern), expected_smudges)    # Vertical symmetry
    return ans


def main():
    import os
    import sys

    # To be able to import the helpers module
    sys.path.append(os.path.dirname(                                        # Project
                        os.path.dirname(                                    # Year
                            os.path.dirname(os.path.abspath(__file__)))))   # Day

    from helpers import Timer

    with open("input.txt", "r") as file:
        patterns = [line.split('\n') for line in file.read().split('\n\n')]

    # --- Part 1 --- #
    with Timer():
        print("Summarizing notes value:", summarize_patterns(patterns, 0))  # 34772

    # --- Part 2 --- #
    with Timer():
        print("Summarizing notes value after smudge fix:", summarize_patterns(patterns, 1))  # 35554


if __name__ == "__main__":
    main()
