# Advent of Code : Day 02 - Rock Paper Scissors
# https://adventofcode.com/2022/day/2

import os
from typing import Dict, List, Tuple, cast

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
def parse(filename: os.PathLike) -> List[Tuple[str, str]]:
    with open(filename, "r") as file:
        guide = [tuple(line.split()) for line in file.read().strip().split("\n")]
    return cast(List[Tuple[str, str]], guide)


@Timer.timeit
def solve(filename: os.PathLike) -> Tuple[int, int]:
    guide = parse(filename)

    part1 = compute_score(guide, score_part1)
    part2 = compute_score(guide, score_part2)

    return part1, part2
