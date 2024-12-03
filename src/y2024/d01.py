# Advent of Code : Day 01 - Historian Hysteria
# https://adventofcode.com/2024/day/01

from collections import Counter

from helpers import Timer, load_input_data


@Timer.timeit
def get_total_distance(l_ids: list[int], r_ids: list[int]) -> int:
    return sum(abs(lhs - rhs) for lhs, rhs in zip(sorted(l_ids), sorted(r_ids)))


@Timer.timeit
def get_similarity_score(l_ids: list[int], r_ids: list[int]) -> int:
    counter = Counter(r_ids)
    return sum(lhs * counter[lhs] for lhs in l_ids if lhs in counter)


@Timer.timeit
def parse(data: str) -> tuple[list[int], list[int]]:
    locations = [tuple(map(int, x.split())) for x in data.splitlines()]

    l_ids = [loc[0] for loc in locations]
    r_ids = [loc[1] for loc in locations]

    return l_ids, r_ids


@Timer.timeit
def solve(data: str) -> tuple[int, int]:
    l_ids, r_ids = parse(data)
    part1 = get_total_distance(l_ids, r_ids)
    part2 = get_similarity_score(l_ids, r_ids)

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2024, 1)))
