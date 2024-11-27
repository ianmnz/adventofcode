# Advent of Code : Day 04 - Scratchcards
# https://adventofcode.com/2023/day/4

import os
import re
from typing import List, Tuple

from helpers import Timer


def compute_card_winnings(numbers: str) -> int:
    winning_nbs, owned_nbs = numbers.split("|")

    winning_nbs = set(winning_nbs.split())
    owned_nbs = set(owned_nbs.split())

    return len(winning_nbs.intersection(owned_nbs))


@Timer.timeit
def compute_total_points(cards: List[str]) -> int:
    total_pts = 0

    for card in cards:
        _, numbers = card.split(":")
        worthiness = compute_card_winnings(numbers)
        total_pts += pow(2, worthiness - 1) if worthiness else 0

    return total_pts


@Timer.timeit
def compute_total_scratchcards(cards: List[str]) -> int:
    total_scratchcards = 0
    scratchcards = [1] * len(cards)

    for card in cards:
        card_id, numbers = card.split(":")
        nb_copies = compute_card_winnings(numbers)

        card_id = int(re.findall(r"\d+", card_id)[0]) - 1
        total_scratchcards += scratchcards[card_id]

        if nb_copies > 0:
            for i in range(1, nb_copies + 1):
                scratchcards[card_id + i] += scratchcards[card_id]

    return total_scratchcards


@Timer.timeit
def parse(filename: os.PathLike) -> List[str]:
    with open(filename, "r") as file:
        cards = file.read().split("\n")
    return cards


@Timer.timeit
def solve(filename: os.PathLike) -> Tuple[int, int]:
    cards = parse(filename)
    part1 = compute_total_points(cards)
    part2 = compute_total_scratchcards(cards)

    return part1, part2
