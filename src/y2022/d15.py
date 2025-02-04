# Advent of Code : Day 15 - Beacon Exclusion Zone
# https://adventofcode.com/2022/day/15

import bisect
import re
from dataclasses import dataclass
from typing import NamedTuple, Self

from helpers import Timer, load_input_data


class Beacon(NamedTuple):
    x: int
    y: int


class Line(NamedTuple):
    # y = m * x + b
    m: int
    b: int


class Sensor(NamedTuple):
    x: int
    y: int
    coverage: int


@dataclass
class Interval:
    lb: int
    ub: int

    def __lt__(self, other: Self) -> bool:
        if self.lb == other.lb:
            return self.ub < other.ub
        return self.lb < other.lb

    def __and__(self, other: Self) -> bool:
        return (other.lb <= self.ub <= other.ub) or (self.lb <= other.ub <= self.ub)

    def __add__(self, other: "Interval") -> "Interval":
        return Interval(min(self.lb, other.lb), max(self.ub, other.ub))

    def __len__(self) -> int:
        return self.ub - self.lb + 1


@Timer.timeit
def build_coverage(coverage: list[str]) -> tuple[list[Sensor], set[Beacon]]:
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
    sensors: list[Sensor],
    row: int,
    lower: float = float("-inf"),
    upper: float = float("inf"),
) -> list[Interval]:
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
    sensors: list[Sensor], beacons: set[Beacon], row: int = 2_000_000
) -> int:
    return sum(len(interval) for interval in _get_row_coverage(sensors, row)) - len(
        [beacon for beacon in beacons if beacon.y == row]
    )


@Timer.timeit
def get_uncovered_position(sensors: list[Sensor], boundary: int = 4_000_000) -> int:
    for y in range(boundary, -1, -1):
        coverage = _get_row_coverage(sensors, y, 0, boundary)

        if len(coverage) == 1:
            continue

        x = coverage[0].ub + 1
        return x * boundary + y

    return -1


@Timer.timeit
def get_uncovered_position_by_line_intersection(
    sensors: list[Sensor], boundary: int = 4_000_000
) -> int:
    # Based on https://www.reddit.com/r/adventofcode/comments/zmcn64/comment/j0b90nr/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
    pos_lines = set()
    neg_lines = set()
    for sensor in sensors:
        neg_lines.add(Line(-1, (sensor.x + sensor.y) + (sensor.coverage + 1)))
        neg_lines.add(Line(-1, (sensor.x + sensor.y) - (sensor.coverage + 1)))

        pos_lines.add(Line(1, (sensor.y - sensor.x) + (sensor.coverage + 1)))
        pos_lines.add(Line(1, (sensor.y - sensor.x) - (sensor.coverage + 1)))

    for pos_line in pos_lines:
        for neg_line in neg_lines:
            x = (neg_line.b - pos_line.b) // 2
            y = (neg_line.b + pos_line.b) // 2

            if (
                (0 <= x <= boundary)
                and (0 <= y <= boundary)
                and all(
                    abs(x - sensor.x) + abs(y - sensor.y) > sensor.coverage
                    for sensor in sensors
                )
            ):
                return x * boundary + y

    return -1


@Timer.timeit
def parse(data: str) -> list[str]:
    return data.strip().split("\n")


@Timer.timeit
def solve(data: str) -> tuple[int, int]:
    coverage = parse(data)
    sensors, beacons = build_coverage(coverage)
    part1 = get_nb_covered_positions_on_row(sensors, beacons)
    # part2 = get_uncovered_position(sensors)
    part2 = get_uncovered_position_by_line_intersection(sensors)

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2022, 15)))
