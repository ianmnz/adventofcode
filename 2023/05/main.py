# Advent of Code : Day 05 - If You Give A Seed A Fertilizer
# https://adventofcode.com/2023/day/5

from typing import List, Tuple, Optional
import re
import time
from dataclasses import dataclass

@dataclass
class Interval:
    left: int
    right: int

    def __lt__(self, other: "Interval") -> bool:
        return self.left < other.left

    def intersect(self, other: "Interval") -> bool:
        return (self.right >= other.left) and (self.left <= other.right)

    def contains(self, other: "Interval") -> bool:
        return self.left <= other.left <= other.right <= self.right

    def left_intersect(self, other: "Interval") -> bool:
        return other.left <= self.left <= other.right < self.right

    def right_intersect(self, other: "Interval") -> bool:
        return self.left < other.left <= self.right <= other.right


def parse() -> Tuple[List[int], List[List[str]]]:
    with open('input.txt', 'r') as file:
        seeds, mappings = file.read().split("\n\n", 1)

    return [int(seed) for seed in re.findall(f"\d+", seeds)], \
           [mapping.split("\n")[1:] for mapping in mappings.split("\n\n")]


def apply(mapping: List[str], domain: List[Interval]) -> List[Interval]:
    images : List[Interval] = list()
    while domain:
        domain_interval = domain.pop()

        for func in mapping:
            destination, source, delta = map(int, func.split())
            mapping_interval = Interval(source, source + delta - 1)
            mapping_shift = destination - source

            if mapping_interval.contains(domain_interval):
                images.append(Interval(domain_interval.left + mapping_shift, domain_interval.right + mapping_shift))
                break

            elif domain_interval.left_intersect(mapping_interval):
                domain.extend([Interval(domain_interval.left, mapping_interval.right),
                               Interval(mapping_interval.right + 1, domain_interval.right)])
                break

            elif domain_interval.right_intersect(mapping_interval):
                domain.extend([Interval(mapping_interval.left, domain_interval.right),
                               Interval(domain_interval.left, mapping_interval.left - 1)])
                break

        else:   # For's else
            images.append(domain_interval)

    return images


def seed_to_location(seeds: List[Interval], mappings: List[List[str]]) -> List[Interval]:
    for mapping in mappings:
        seeds = apply(mapping, seeds)
    return seeds


def main():
    seeds, mappings = parse()

    # --- Part 1 --- #
    t_start = time.perf_counter_ns()
    seed_intervals = [Interval(seed, seed) for seed in seeds]
    print("Lowest location number:", min(seed_to_location(seed_intervals, mappings)).left)     # 650599855
    t_end = time.perf_counter_ns()
    print(f"Elapsed time: {(t_end - t_start) * 1.e-6:.3f} ms")

    # --- Part 2 --- #
    t_start = time.perf_counter_ns()
    seed_intervals = [Interval(seed, seed + delta -1) for seed, delta in zip(seeds[::2], seeds[1::2])]
    print("Lowest location number (Part 2):", min(seed_to_location(seed_intervals, mappings)).left)     #1240035
    t_end = time.perf_counter_ns()
    print(f"Elapsed time (Part 2): {(t_end - t_start) * 1.e-6:.3f} ms")


if __name__ == "__main__":
    main()
