# Advent of Code : Day 02 - Gift Shop
# https://adventofcode.com/2025/day/2

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


def is_in_any_range(id_ranges: Iterable[Interval], candidate: int) -> bool:
    lower, upper = 0, len(id_ranges) - 1

    while lower <= upper:
        mid = (lower + upper) // 2

        if candidate > id_ranges[mid][1]:
            lower = mid + 1
        elif candidate < id_ranges[mid][0]:
            upper = mid - 1
        else:
            return True

    return False


def sum_invalid_ids(id_ranges: Iterable[Interval]) -> tuple[int, int]:
    invalids = []
    mirrored = []

    min_invalid_id = id_ranges[0][0]
    max_invalid_id = id_ranges[-1][1]

    for i in range(1, 100_000):  # magic number
        for repeat in range(2, 11):  # magic number
            candidate = int(str(i) * repeat)

            if candidate < min_invalid_id or max_invalid_id < candidate:
                break

            if is_in_any_range(id_ranges, candidate):
                invalids.append(candidate)
                if repeat == 2:
                    mirrored.append(candidate)

    return sum(set(mirrored)), sum(set(invalids))


@Timer.timeit
def parse(data: str) -> list[Interval]:
    return [tuple(map(int, id_ranges.split("-"))) for id_ranges in data.split(",")]


@Timer.timeit
def solve(data: str) -> tuple[int, int]:
    id_ranges = merge_intervals(parse(data))
    part1, part2 = sum_invalid_ids(id_ranges)

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2025, 2)))
