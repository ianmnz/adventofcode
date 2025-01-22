# Advent of Code : Day 02 - Rock Paper Scissors
# https://adventofcode.com/2022/day/2

from typing import cast

from helpers import Timer, load_input_data

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
    guide: list[tuple[str, str]], score_map: dict[str, dict[str, int]]
) -> int:
    return sum(score_map[opponent][player] for opponent, player in guide)


@Timer.timeit
def parse(data: str) -> list[tuple[str, str]]:
    guide = [tuple(line.split()) for line in data.strip().split("\n")]
    return cast(list[tuple[str, str]], guide)


@Timer.timeit
def solve(data: str) -> tuple[int, int]:
    guide = parse(data)

    part1 = compute_score(guide, score_part1)
    part2 = compute_score(guide, score_part2)

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2022, 2)))
