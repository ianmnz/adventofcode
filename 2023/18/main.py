# Advent of Code : Day 18 - Lavaduct Lagoon
# https://adventofcode.com/2023/day/18

from typing import List, Tuple


direction = {
    'R': ( 0, 1), '0': ( 0, 1),
    'D': ( 1, 0), '1': ( 1, 0),
    'L': ( 0,-1), '2': ( 0,-1),
    'U': (-1, 0), '3': (-1, 0)
}


def dig(plan: List[List[str]], is_color_code: bool = False) -> int:
    def parse(command: List[str]) -> Tuple[int]:
        dir, length, color = command

        if not is_color_code:
            return *direction[dir], int(length)
        else:
            return *direction[color[7]], int(color[2:7], 16)

    row, col, area = 0, 0, 0
    for command in plan:
        dx, dy, length = parse(command)

        row += length * dx
        col += length * dy

        # internal area + half perimeter
        area += (col * dx * length) + (length/2)

    return int(area + 1)


def main():
    import os
    import sys

    # To be able to import the helpers module
    sys.path.append(os.path.dirname(                                        # Project
                        os.path.dirname(                                    # Year
                            os.path.dirname(os.path.abspath(__file__)))))   # Day

    from helpers import Timer

    with open("input.txt", "r") as file:
        plan = [line.split() for line in file.read().split('\n')]

    # --- Part 1 --- #
    with Timer():
        print("Digged area:", dig(plan))  # 50603

    # --- Part 2 --- #
    with Timer():
        print("Digged area with color-code:", dig(plan, True))  # 96556251590677


if __name__ == "__main__":
    main()
