# Advent of Code : Day 22 - Sand Slabs
# https://adventofcode.com/2023/day/22

import collections
from typing import List, Iterable, Tuple, Set, Dict
from dataclasses import dataclass, field


Position = collections.namedtuple('Position', ['x', 'y', 'z'])

@dataclass
class Brick:
    left: Position
    right: Position

    stack_up: Set['Brick'] = field(init=False, default_factory=lambda: set(), repr=False)
    stack_on: Set['Brick'] = field(init=False, default_factory=lambda: set(), repr=False)

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

    def stackpush(self, above: 'Brick') -> None:
        self.stack_up.add(above)
        above.stack_on.add(self)

    def __lt__(self, other: 'Brick') -> bool:
        return self.base() < other.base()

    def __hash__(self) -> int:
        return hash((*self.left, *self.right))

    def __eq__(self, other: 'Brick') -> bool:
        return self.left == other.left and self.right == other.right


def simulate(bricks: List[Brick]) -> List[Brick]:
    top_down_view = dict()
    settled = []

    for brick in bricks:
        peak = max(top_down_view[(x, y)].top() if (x,y) in top_down_view else 0 for x, y in brick.shadow())
        height = max(0, brick.base() - peak - 1)

        if height > 0:
            brick = brick.drop(height)

        settled.append(brick)

        for x, y in brick.shadow():
            if (x, y) in top_down_view and top_down_view[(x, y)].top() == brick.base() - 1:
                top_down_view[(x, y)].stackpush(brick)
            top_down_view[(x, y)] = brick

    return settled


def count_falls_if_removed(brick: Brick, support: Dict[Brick, int]) -> int:
    fallen = [brick]
    nb_falls = 0
    while fallen:
        base = fallen.pop()

        for stacked_up in base.stack_up:
            support[stacked_up] -= 1

            if support[stacked_up] == 0:
                fallen.append(stacked_up)
                nb_falls += 1

    return nb_falls


def bricks_to_disintegrate(data: List[Brick]) -> Tuple[int]:
    settled = simulate(sorted(data))

    safe = 0
    count = 0
    support = {brick: len(brick.stack_on) for brick in settled}

    for brick in settled:
        nb_falls = count_falls_if_removed(brick, support.copy())
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
        print("Nb of brick to disintegrate:", bricks_to_disintegrate(data)[0])  # 468

    # --- Part 2 --- #
    with Timer():
        print("Nb of brick to disintegrate:", bricks_to_disintegrate(data)[1])  # 75358


if __name__ == "__main__":
    main()
