# Advent of Code : Day 04 - Scratchcards
# https://adventofcode.com/2023/day/4

import re
from typing import List, Tuple


def compute_card_winnings(numbers: str) -> int:
    winning_nbs, owned_nbs = numbers.split('|')

    winning_nbs = set(winning_nbs.split())
    owned_nbs = set(owned_nbs.split())

    return len(winning_nbs.intersection(owned_nbs))


def compute_total_points(cards: List[str]) -> int:
    total_pts = 0

    for card in cards:
        _, numbers = card.split(':')
        worthiness = compute_card_winnings(numbers)
        total_pts +=  pow(2, worthiness - 1) if worthiness else 0

    return total_pts


def compute_total_scratchcards(cards: List[str]) -> int:
    total_scratchcards = 0
    scratchcards = [1] * len(cards)

    for card in cards:
        card_id, numbers = card.split(':')
        nb_copies = compute_card_winnings(numbers)

        card_id = int(re.findall(f'\d+', card_id)[0]) - 1
        total_scratchcards += scratchcards[card_id]

        if nb_copies > 0:
            for i in range(1, nb_copies + 1):
                scratchcards[card_id + i] += scratchcards[card_id]

    return total_scratchcards


def solve(filename: str) -> Tuple[int, int]:
    with open(filename, "r") as file:
        cards = file.read().split('\n')

    part1 = compute_total_points(cards)
    part2 = compute_total_scratchcards(cards)

    return part1, part2


def main():
    import os
    from helpers import Timer

    with Timer():
        res = solve(os.path.dirname(os.path.abspath(__file__)) + "/input.txt")

        assert res[0] == 24733,   f"Part1 = {res[0]}"
        assert res[1] == 5422730, f"Part2 = {res[1]}"


if __name__ == "__main__":
    main()
