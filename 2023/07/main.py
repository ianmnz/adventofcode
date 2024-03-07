# Advent of Code : Day 07 - Camel Cards
# https://adventofcode.com/2023/day/7

from collections import defaultdict
from dataclasses import dataclass, field
from typing import List, Tuple

from helpers import Timer

hand_strength = {
    "high": 1,
    "pair": 2,
    "two pairs": 3,
    "three": 4,
    "full house": 5,
    "four": 6,
    "five": 7,
}


card_strength = {
    "2": 1,
    "3": 2,
    "4": 3,
    "5": 4,
    "6": 5,
    "7": 6,
    "8": 7,
    "9": 8,
    "T": 9,
    "J": 10,
    "Q": 11,
    "K": 12,
    "A": 13,
}


@dataclass
class Hand:
    cards: str
    bid: int
    rank: int = field(init=False, repr=False)

    def __lt__(self, other: "Hand") -> bool:
        if self.rank == other.rank:
            for self_card, other_card in zip(self.cards, other.cards):
                if card_strength[self_card] == card_strength[other_card]:
                    continue
                else:
                    return card_strength[self_card] < card_strength[other_card]
        else:
            return self.rank < other.rank

    def set_rank(self, with_joker: bool = False) -> None:
        counter = defaultdict(int)

        for card in self.cards:
            counter[card] += 1

        # For a case like 'JJJJJ'
        if with_joker and ("J" in counter) and (counter["J"] != 5):
            nb_jokers = counter["J"]
            del counter["J"]
            counter[max(counter, key=counter.get)] += nb_jokers

        nb_unique = len(counter)

        if nb_unique == 1:
            self.rank = hand_strength["five"]

        elif nb_unique == 2:
            if {2, 3} <= set(counter.values()):
                self.rank = hand_strength["full house"]
            else:  # {1, 4}
                self.rank = hand_strength["four"]

        elif nb_unique == 3:
            if {1, 3} <= set(counter.values()):
                self.rank = hand_strength["three"]
            else:  # {1, 2}
                self.rank = hand_strength["two pairs"]

        elif nb_unique == 4:
            self.rank = hand_strength["pair"]

        else:
            self.rank = hand_strength["high"]


@Timer.timeit
def calculate_total_winnings(hands: List[Hand]) -> int:
    total_winnings = 0
    for i, hand in enumerate(hands, 1):
        total_winnings += i * hand.bid
    return total_winnings


@Timer.timeit
def set_ranks(hands: List[Hand], with_joker: bool = False) -> None:
    for hand in hands:
        hand.set_rank(with_joker)


@Timer.timeit
def parse(filename: str) -> List[Hand]:
    with open(filename, "r") as file:
        hands = [
            Hand(hand[0], int(hand[1]))
            for hand in map(lambda ss: ss.strip().split(), file.read().split("\n"))
        ]
    return hands


@Timer.timeit
def solve(filename: str) -> Tuple[int, int]:
    hands = parse(filename)

    set_ranks(hands)
    part1 = calculate_total_winnings(sorted(hands))

    card_strength["J"] = 0
    set_ranks(hands, True)
    part2 = calculate_total_winnings(sorted(hands))

    return part1, part2


def main():
    import os

    res = solve(os.path.dirname(os.path.abspath(__file__)) + "/input.txt")

    assert res[0] == 253910319, f"Part1 = {res[0]}"
    assert res[1] == 254083736, f"Part2 = {res[1]}"


if __name__ == "__main__":
    main()
