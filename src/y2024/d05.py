# Advent of Code : Day 05 - Print Queue
# https://adventofcode.com/2024/day/05

from dataclasses import dataclass, field
from typing import Self

from helpers import Timer, load_input_data


@dataclass
class Order:
    x: int
    precedes: set[int] = field(default_factory=set)

    def __or__(self, other: Self) -> None:
        self.precedes.add(other.x)

    def __lt__(self, other: Self) -> bool:
        return other.x in self.precedes


@Timer.timeit
def get_middle_pages(
    ordering: dict[int, Order], updates: list[list[int]]
) -> tuple[int, int]:
    correctly_ordered = 0
    incorrectly_ordered = 0

    for update in updates:
        # assert len(update) % 2 == 1
        # assert all(page in ordering for page in update)

        ordered = sorted(update, key=lambda x: ordering[x])

        if update != ordered:
            incorrectly_ordered += ordered[len(ordered) // 2]

        else:
            correctly_ordered += update[len(update) // 2]

    return correctly_ordered, incorrectly_ordered


@Timer.timeit
def parse(data: str) -> tuple[dict[int, Order], list[list[int]]]:
    rules, updates = data.split("\n\n")

    ordering: dict[int, Order] = {}
    for rule in rules.splitlines():
        x, y = map(int, rule.split("|"))

        X = ordering.setdefault(x, Order(x))
        Y = ordering.setdefault(y, Order(y))

        X | Y  # type: ignore

    return ordering, [
        [int(x) for x in update.split(",")] for update in updates.splitlines()
    ]


@Timer.timeit
def solve(data: str) -> tuple[int, int]:
    ordering, updates = parse(data)
    part1, part2 = get_middle_pages(ordering, updates)

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2024, 5)))
