# Advent of Code : Day 09 - Movie Theater
# https://adventofcode.com/2025/day/09

from collections.abc import Iterable
from typing import NamedTuple

from helpers import Timer, load_input_data


class Pos2D(NamedTuple):
    x: int
    y: int


class Rectangle:
    x_min: int
    x_max: int
    y_min: int
    y_max: int

    area: int

    def __init__(self, A: Pos2D, B: Pos2D) -> None:
        self.x_min, self.x_max = min(A.x, B.x), max(A.x, B.x)
        self.y_min, self.y_max = min(A.y, B.y), max(A.y, B.y)
        self.area = (abs(A.x - B.x) + 1) * (abs(A.y - B.y) + 1)

    def intersect(self, other: "Rectangle") -> bool:
        return not (
            self.x_max <= other.x_min
            or other.x_max <= self.x_min
            or self.y_max <= other.y_min
            or other.y_max <= self.y_min
        )


# TODO Too slow. Find a better algorithm
def get_largest_rectangle_area(positions: Iterable[Pos2D]) -> tuple[int, int]:
    n = len(positions)

    edges = [Rectangle(positions[i], positions[i - 1]) for i in range(n)]

    rectangles = sorted(
        (
            Rectangle(positions[i], positions[j])
            for i in range(n)
            for j in range(i + 1, n)
        ),
        reverse=True,
        key=lambda rect: rect.area,
    )

    any_max = rectangles[0].area
    constraint_max = 0

    for rect in rectangles:
        if not any(rect.intersect(other) for other in edges):
            constraint_max = rect.area
            break

    return any_max, constraint_max


@Timer.timeit
def parse(data: str) -> list[Pos2D]:
    return [Pos2D(*map(int, row.split(","))) for row in data.split("\n")]


@Timer.timeit
def solve(data: str) -> tuple[int, int]:
    positions = parse(data)
    part1, part2 = get_largest_rectangle_area(positions)

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2025, 9)))
