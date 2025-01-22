# Advent of Code : Day 05 - If You Give A Seed A Fertilizer
# https://adventofcode.com/2023/day/5

import re
from dataclasses import dataclass
from typing import Self

from helpers import Timer, load_input_data


@dataclass
class Interval:
    left: int
    right: int

    def __lt__(self, other: Self) -> bool:
        return self.left < other.left

    def intersect(self, other: Self) -> bool:
        return (self.right >= other.left) and (self.left <= other.right)

    def contains(self, other: Self) -> bool:
        return self.left <= other.left <= other.right <= self.right

    def left_intersect(self, other: Self) -> bool:
        return other.left <= self.left <= other.right < self.right

    def right_intersect(self, other: Self) -> bool:
        return self.left < other.left <= self.right <= other.right


def apply(mapping: list[str], domain: list[Interval]) -> list[Interval]:
    images: list[Interval] = list()
    while domain:
        domain_interval = domain.pop()

        for func in mapping:
            destination, source, delta = map(int, func.split())
            mapping_interval = Interval(source, source + delta - 1)
            mapping_shift = destination - source

            if mapping_interval.contains(domain_interval):
                images.append(
                    Interval(
                        domain_interval.left + mapping_shift,
                        domain_interval.right + mapping_shift,
                    )
                )
                break

            elif domain_interval.left_intersect(mapping_interval):
                domain.extend(
                    [
                        Interval(domain_interval.left, mapping_interval.right),
                        Interval(mapping_interval.right + 1, domain_interval.right),
                    ]
                )
                break

            elif domain_interval.right_intersect(mapping_interval):
                domain.extend(
                    [
                        Interval(mapping_interval.left, domain_interval.right),
                        Interval(domain_interval.left, mapping_interval.left - 1),
                    ]
                )
                break

        else:  # For's else
            images.append(domain_interval)

    return images


@Timer.timeit
def seed_to_location(
    seeds: list[Interval], mappings: list[list[str]]
) -> list[Interval]:
    for mapping in mappings:
        seeds = apply(mapping, seeds)
    return seeds


@Timer.timeit
def parse(data: str) -> tuple[list[int], list[list[str]]]:
    seeds, mappings = data.split("\n\n", 1)

    seeds = [int(seed) for seed in re.findall(r"\d+", seeds)]
    mappings = [mapping.split("\n")[1:] for mapping in mappings.split("\n\n")]

    return seeds, mappings


@Timer.timeit
def solve(data: str) -> tuple[int, int]:
    seeds, mappings = parse(data)

    seed_intervals = [Interval(seed, seed) for seed in seeds]
    part1 = min(seed_to_location(seed_intervals, mappings)).left

    seed_intervals = [
        Interval(seed, seed + delta - 1) for seed, delta in zip(seeds[::2], seeds[1::2])
    ]
    part2 = min(seed_to_location(seed_intervals, mappings)).left

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2023, 5)))
