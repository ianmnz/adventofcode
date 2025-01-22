# Advent of Code : Day 09 - Rope Bridge
# https://adventofcode.com/2022/day/9

from dataclasses import dataclass, field
from typing import Self

from helpers import Timer, load_input_data

RIGHT = 1 + 0j
LEFT = -1 + 0j
UP = 0 + 1j
DOWN = 0 - 1j


@dataclass
class Knot:
    pos: complex

    prev: None | Self = field(default=None)
    next: None | Self = field(init=False, default=None)
    visited: set[complex] = field(init=False)

    def __post_init__(self) -> None:
        self.visited = {self.pos}

        if self.prev is not None:
            self.prev.next = self

    def move(self, to: str) -> None:
        direction = 0j

        if "L" in to:
            direction += LEFT
        if "R" in to:
            direction += RIGHT
        if "U" in to:
            direction += UP
        if "D" in to:
            direction += DOWN

        self.pos += direction
        self.visited.add(self.pos)

        if self.next is not None:
            self.next._follow()

    def _follow(self) -> None:
        if (self.prev is None) or are_adjacent(self, self.prev):
            return

        rel_pos = relative_position(self, self.prev)

        if rel_pos.real * rel_pos.imag == 0:
            # Same row or col
            if rel_pos.real > 0:
                self.move("R")
            elif rel_pos.real < 0:
                self.move("L")
            elif rel_pos.imag > 0:
                self.move("U")
            elif rel_pos.imag < 0:
                self.move("D")

        elif rel_pos.real * rel_pos.imag > 0:
            # Diagonally
            if rel_pos.real > 0:  # 1st quadrant
                self.move("RU")
            else:  # 3rd quadrant
                self.move("LD")

        else:
            # Diagonally
            if rel_pos.real > 0:  # 2nd quadrant
                self.move("RD")
            else:  # 4th quadrant
                self.move("LU")


def relative_position(this: Knot, that: Knot) -> complex:
    return that.pos - this.pos


def are_adjacent(this: Knot, that: Knot) -> bool:
    rel_pos = relative_position(this, that)
    return abs(rel_pos.real) <= 1 and abs(rel_pos.imag) <= 1


@dataclass
class Rope:
    head: None | Knot = field(default=None)
    tail: None | Knot = field(default=None)

    def move(self, to: str, dist: int) -> None:
        if self.head is None:
            return

        for _ in range(dist):
            self.head.move(to)

    def insert_knot(self, start: complex = 0j) -> None:
        if self.head is None:
            self.head = Knot(start)

        elif self.tail is None:
            self.tail = Knot(start, self.head)

        else:
            self.tail.next = Knot(start, self.tail)
            self.tail = self.tail.next


@Timer.timeit
def build_rope(nb_knots: int) -> Rope:
    rope = Rope()
    for _ in range(nb_knots):
        rope.insert_knot()
    return rope


@Timer.timeit
def get_nb_visited_positions_by_tail(motions: list[str], nb_knots: int) -> int:
    rope = build_rope(nb_knots)
    for motion in motions:
        to, dist = motion.strip().split()
        rope.move(to, int(dist))

    if rope.tail is None:
        return -1
    else:
        return len(rope.tail.visited)


@Timer.timeit
def parse(data: str) -> list[str]:
    return data.strip().split("\n")


@Timer.timeit
def solve(data: str) -> tuple[int, int]:
    motions = parse(data)
    part1 = get_nb_visited_positions_by_tail(motions, 2)
    part2 = get_nb_visited_positions_by_tail(motions, 10)

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2022, 9)))
