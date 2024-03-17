# Advent of Code : Day 15 - Beacon Exclusion Zone
# https://adventofcode.com/2022/day/15

import bisect
import re
from dataclasses import dataclass
from typing import List, NamedTuple, Set, Tuple

from helpers import Timer


class Beacon(NamedTuple):
    x: int
    y: int


class Sensor(NamedTuple):
    x: int
    y: int
    coverage: int


@dataclass
class Interval:
    lb: int
    ub: int

    def __lt__(self, other: "Interval") -> bool:
        if self.lb == other.lb:
            return self.ub < other.ub
        return self.lb < other.lb

    def __and__(self, other: "Interval") -> bool:
        return (other.lb <= self.ub <= other.ub) or (self.lb <= other.ub <= self.ub)

    def __add__(self, other: "Interval") -> "Interval":
        return Interval(min(self.lb, other.lb), max(self.ub, other.ub))

    def __len__(self) -> int:
        return self.ub - self.lb + 1


@Timer.timeit
def build_coverage(coverage: List[str]) -> Tuple[List[Sensor], Set[Beacon]]:
    sensors = []
    beacons = set()
    pattern = re.compile(
        r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)"
    )

    for sensor in coverage:
        match = pattern.match(sensor)
        if match is not None:
            sensor_x, sensor_y = int(match.group(1)), int(match.group(2))
            beacon_x, beacon_y = int(match.group(3)), int(match.group(4))
            distance = abs(beacon_x - sensor_x) + abs(beacon_y - sensor_y)

            sensors.append(Sensor(sensor_x, sensor_y, distance))
            beacons.add(Beacon(beacon_x, beacon_y))

    return sensors, beacons


def _get_row_coverage(
    sensors: List[Sensor],
    row: int,
    lower: float = float("-inf"),
    upper: float = float("inf"),
) -> List[Interval]:
    intervals = []
    for sensor in sensors:
        x_margin = sensor.coverage - abs(row - sensor.y)
        if x_margin >= 0:
            # We keep only those intervals that cover
            # some part of the row and sort them
            lb = int(max(lower, sensor.x - x_margin))
            ub = int(min(upper, sensor.x + x_margin))
            bisect.insort(intervals, Interval(lb, ub))

    # We fuse intercepting intervals
    # Since they are already sorted,
    # we only need to check the current
    # interval against the top of the stack
    fused_intervals = [intervals[0]]
    for interval in intervals[1:]:
        top = fused_intervals.pop()
        if top & interval:
            fused_intervals.append(top + interval)
        else:
            fused_intervals.append(top)
            fused_intervals.append(interval)

    return fused_intervals


@Timer.timeit
def get_nb_covered_positions_on_row(
    sensors: List[Sensor], beacons: Set[Beacon], row: int = 2_000_000
) -> int:
    return sum(len(interval) for interval in _get_row_coverage(sensors, row)) - len(
        [beacon for beacon in beacons if beacon.y == row]
    )


@Timer.timeit
def get_uncovered_position(sensors: List[Sensor], boundary: int = 4_000_000) -> int:
    for y in range(boundary, -1, -1):
        coverage = _get_row_coverage(sensors, y, 0, boundary)

        if len(coverage) == 1:
            continue

        x = coverage[0].ub + 1
        return x * boundary + y

    return -1


@Timer.timeit
def parse(filename: str) -> List[str]:
    with open(filename, "r") as file:
        coverage = file.read().strip().split("\n")
    return coverage


@Timer.timeit
def solve(filename: str) -> Tuple[int, int]:
    coverage = parse(filename)
    sensors, beacons = build_coverage(coverage)
    part1 = get_nb_covered_positions_on_row(sensors, beacons)
    part2 = get_uncovered_position(sensors)

    return part1, part2


def main() -> None:
    import os

    res = solve(os.path.dirname(os.path.abspath(__file__)) + "/input.txt")

    assert res[0] == 4_725_496, f"Part1 = {res[0]}"
    assert res[1] == 12_051_287_042_458, f"Part2 = {res[1]}"


if __name__ == "__main__":
    main()
