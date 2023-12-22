# Advent of Code : Day 22 - Sand Slabs
# https://adventofcode.com/2023/day/22

import collections
from typing import List, Iterable, Tuple
from dataclasses import dataclass


Position = collections.namedtuple('Position', ['x', 'y', 'z'])

@dataclass
class Brick:
    left: Position
    right: Position

    def base(self) -> int:
        return min(self.left.z, self.right.z)

    def top(self) -> int:
        return max(self.left.z, self.right.z)

    def shadow(self) -> Iterable:
        for x in range(self.left.x, self.right.x + 1):
            for y in range(self.left.y, self.right.y + 1):
                yield (x, y)

    def drop(self, height: int) -> 'Brick':
        return Brick(Position(self.left.x, self.left.y, self.left.z - height),
                     Position(self.right.x, self.right.y, self.right.z - height))

    def __lt__(self, other: 'Brick') -> bool:
        return self.base() < other.base()


def simulate(bricks: List[Brick]) -> Tuple[int, List[Brick]]:
    top_down_view = collections.defaultdict(int)
    settled = []
    nb_falls = 0

    for brick in bricks:
        peak = max(top_down_view[(x, y)] for x, y in brick.shadow())
        height = max(0, brick.base() - peak - 1)

        if height > 0:
            nb_falls += 1
            brick = brick.drop(height)

        settled.append(brick)

        for x, y in brick.shadow():
            top_down_view[(x, y)] = brick.top()

    return nb_falls, settled


def bricks_to_disintegrate(data: List[Brick]) -> Tuple[int]:
    _, settled = simulate(sorted(data))

    safe = 0
    count = 0
    for idx in range(len(settled)):
        stack = settled[:idx] + settled[idx + 1:]
        nb_falls, _ = simulate(stack)
        safe += int(nb_falls == 0)
        count += nb_falls

    return safe, count


def main():
    import os
    import sys

    # To be able to import the helpers module
    sys.path.append(os.path.dirname(                                        # Project
                        os.path.dirname(                                    # Year
                            os.path.dirname(os.path.abspath(__file__)))))   # Day

    from helpers import Timer

    with open("input.txt", "r") as file:
        snapshot = [line.split('~') for line in file.read().split('\n')]

        data = []
        for left, right in snapshot:
            left = Position(*eval(left))
            right = Position(*eval(right))
            data.append(Brick(left, right))

    # --- Part 1 --- #
    with Timer():
        # print(solve(snapshot))
        print("Nb of brick to disintegrate:", bricks_to_disintegrate(data)[0])  # 468

    # --- Part 2 --- #
    with Timer():
        print("Nb of brick to disintegrate:", bricks_to_disintegrate(data)[1])  # 75358


if __name__ == "__main__":
    main()
