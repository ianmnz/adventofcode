# Advent of Code : Day 05 - Cafeteria
# https://adventofcode.com/2025/day/5

import re
from collections.abc import Iterable
from operator import itemgetter

from helpers import Timer, load_input_data

Interval = tuple[int, int]


def merge_intervals(intervals: Iterable[Interval]) -> Iterable[Interval]:
    merged = []

    intervals = sorted(intervals, key=itemgetter(0))

    merged.append(intervals[0])

    prev_l, prev_r = merged[-1]
    for curr_l, curr_r in intervals[1:]:
        if curr_l <= prev_r:
            prev_r = max(prev_r, curr_r)
            merged[-1] = (prev_l, prev_r)
        else:
            merged.append((curr_l, curr_r))
            prev_l, prev_r = curr_l, curr_r

    return merged


"""
def count_available_fresh_ingredients(
        intervals: Iterable[Interval],
        ingredients: Iterable[int]
    ) -> int:
    return sum(
        any(lft <= ingredient <= rgt for lft, rgt in intervals)
        for ingredient in ingredients
    )
"""


def count_available_fresh_ingredients(
    intervals: Iterable[Interval], ingredients: Iterable[int]
) -> int:
    count = 0

    idx_itv, idx_igd = 0, 0
    lft, rgt = intervals[0]

    while idx_itv < len(intervals) and idx_igd < len(ingredients):
        ingredient = ingredients[idx_igd]

        if ingredient <= rgt:
            # Current ingredient is
            # either before current interval (ingredient < lft)
            # or inside the current interval (lft <= ingredient <= rgt)
            # We advance its iterator either case
            if lft <= ingredient:
                # Current ingredient is fresh.
                count += 1
            idx_igd += 1

        else:
            # Current ingredient has
            # already passed current interval (rgt < ingredient)
            # We advance the interval's iterator
            idx_itv += 1
            lft, rgt = intervals[idx_itv]

    # If any ingredient left, compare them with last interval
    return count + sum(lft <= ingredient <= rgt for ingredient in ingredients[idx_igd:])


def count_all_possible_fresh_ingredients(intervals: Iterable[Interval]) -> int:
    return sum(rgt - lft + 1 for lft, rgt in intervals)


@Timer.timeit
def parse(data: str) -> tuple[Iterable[Interval], Iterable[int]]:
    intervals, ingredients = data.split("\n\n")
    return (
        [(int(lhs), int(rhs)) for lhs, rhs in re.findall(r"(\d+)-(\d+)", intervals)],
        sorted(map(int, ingredients.split("\n"))),
    )


@Timer.timeit
def solve(data: str) -> tuple[int, int]:
    intervals, ingredients = parse(data)
    intervals = merge_intervals(intervals)
    part1 = count_available_fresh_ingredients(intervals, ingredients)
    part2 = count_all_possible_fresh_ingredients(intervals)

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2025, 5)))
