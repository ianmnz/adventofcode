# Advent of Code : Day 03 - Rucksack Reorganization
# https://adventofcode.com/2022/day/3

import os
from itertools import islice
from typing import Generator, Iterable

from helpers import Timer


def priority(item: str) -> int:
    prio = {
        "a": 1,
        "b": 2,
        "c": 3,
        "d": 4,
        "e": 5,
        "f": 6,
        "g": 7,
        "h": 8,
        "i": 9,
        "j": 10,
        "k": 11,
        "l": 12,
        "m": 13,
        "n": 14,
        "o": 15,
        "p": 16,
        "q": 17,
        "r": 18,
        "s": 19,
        "t": 20,
        "u": 21,
        "v": 22,
        "w": 23,
        "x": 24,
        "y": 25,
        "z": 26,
    }
    if item.isupper():
        return 26 + prio[item.lower()]
    else:
        return prio[item]


@Timer.timeit
def find_priority_of_common(rucksacks: list[str]) -> int:
    sum_common_type_prio = 0

    for rucksack in rucksacks:
        middle = len(rucksack) // 2
        common = set(rucksack[:middle]) & set(rucksack[middle:])
        sum_common_type_prio += priority(list(common)[0])

    return sum_common_type_prio


@Timer.timeit
def find_priority_of_badges(rucksacks: list[str]) -> int:
    def batched(iterable: Iterable, chunk_size: int) -> Generator[tuple, None, None]:
        iterator = iter(iterable)
        while chunk := tuple(islice(iterator, chunk_size)):
            yield chunk

    sum_badge_type_prio = 0

    for first, second, third in batched(rucksacks, 3):
        badge = set(first) & set(second) & set(third)
        sum_badge_type_prio += priority(list(badge)[0])

    return sum_badge_type_prio


@Timer.timeit
def parse(filename: os.PathLike) -> list[str]:
    with open(filename, "r") as file:
        rucksacks = file.read().strip().split()
    return rucksacks


@Timer.timeit
def solve(filename: os.PathLike) -> tuple[int, int]:
    rucksacks = parse(filename)
    part1 = find_priority_of_common(rucksacks)
    part2 = find_priority_of_badges(rucksacks)

    return part1, part2
