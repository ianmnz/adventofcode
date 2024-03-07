# Advent of Code : Day 02 - Rock Paper Scissors
# https://adventofcode.com/2022/day/2

from typing import Dict, List, Tuple

from helpers import Timer

score_part1 = {
    "A": {"X": 4, "Y": 8, "Z": 3},
    "B": {"X": 1, "Y": 5, "Z": 9},
    "C": {"X": 7, "Y": 2, "Z": 6},
}


score_part2 = {
    "A": {"X": 3, "Y": 4, "Z": 8},
    "B": {"X": 1, "Y": 5, "Z": 9},
    "C": {"X": 2, "Y": 6, "Z": 7},
}


@Timer.timeit
def compute_score(
    guide: List[Tuple[str, str]], score_map: Dict[str, Dict[str, int]]
) -> int:
    return sum(score_map[opponent][player] for opponent, player in guide)


@Timer.timeit
def parse(filename: str) -> List[Tuple[str, str]]:
    with open(filename, "r") as file:
        guide = [line.split() for line in file.read().strip().split("\n")]
    return guide


@Timer.timeit
def solve(filename: str) -> Tuple[int, int]:
    guide = parse(filename)

    part1 = compute_score(guide, score_part1)
    part2 = compute_score(guide, score_part2)

    return part1, part2


def main() -> None:
    import os

    res = solve(os.path.dirname(os.path.abspath(__file__)) + "/input.txt")

    assert res[0] == 11873, f"Part1 = {res[0]}"
    assert res[1] == 12014, f"Part2 = {res[1]}"


if __name__ == "__main__":
    main()
