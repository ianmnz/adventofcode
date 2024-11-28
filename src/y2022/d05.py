# Advent of Code : Day 05 - Supply Stacks
# https://adventofcode.com/2022/day/5

import collections
import copy
import os
import re
from typing import NamedTuple

from helpers import Timer


class Move(NamedTuple):
    nb: int  # Nb of crates moved
    fr: int  # Origin stack
    to: int  # Destination stack


@Timer.timeit
def move_crates_changing_order(
    stacks: dict[int, collections.deque], moves: list[Move]
) -> None:
    for move in moves:
        for _ in range(move.nb):
            crate = stacks[move.fr].pop()
            stacks[move.to].append(crate)


@Timer.timeit
def move_crates_preserving_order(
    stacks: dict[int, collections.deque], moves: list[Move]
) -> None:
    for move in moves:
        moved_crates = []
        for _ in range(move.nb):
            crate = stacks[move.fr].pop()
            moved_crates.append(crate)

        while moved_crates:
            crate = moved_crates.pop()
            stacks[move.to].append(crate)


@Timer.timeit
def read_top_of_stacks(stacks: dict[int, collections.deque]) -> str:
    return "".join(stacks[key][-1] for key in sorted(stacks.keys()))


@Timer.timeit
def parse(filename: os.PathLike) -> tuple[dict[int, collections.deque], list[Move]]:
    with open(filename, "r") as file:
        initial_arrangement, rearrangements = file.read().strip().split("\n\n")

    spacing = 4
    stacks = collections.defaultdict(collections.deque)
    for line in initial_arrangement.split("\n")[:-1]:
        for i, crate in enumerate(
            (
                line[i : i + spacing].strip().lstrip("[").rstrip("]")
                for i in range(0, len(line), spacing)
            ),
            1,
        ):
            if crate:
                stacks[i].appendleft(crate)

    pattern = re.compile(r"move (\d+) from (\d+) to (\d+)")
    moves = []
    for line in rearrangements.split("\n"):
        match = pattern.match(line)

        if match is None:
            continue

        moves.append(
            Move(int(match.group(1)), int(match.group(2)), int(match.group(3)))
        )

    return stacks, moves


@Timer.timeit
def solve(filename: os.PathLike) -> tuple[str, str]:
    stacks, moves = parse(filename)
    stacks_cp = copy.deepcopy(stacks)

    move_crates_changing_order(stacks, moves)
    move_crates_preserving_order(stacks_cp, moves)

    part1 = read_top_of_stacks(stacks)
    part2 = read_top_of_stacks(stacks_cp)

    return part1, part2
