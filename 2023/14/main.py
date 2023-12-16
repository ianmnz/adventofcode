# Advent of Code : Day 14 - Parabolic Reflector Dish
# https://adventofcode.com/2023/day/14

from typing import List


def rotate(platform: List[List[str]]) -> List[List[str]]:
    # rotate 90° clockwise
    return [[platform[j][i] for j in range(len(platform) - 1, -1, -1)]
                            for i in range(len(platform[0]))]


def tilt(platform: List[List[str]]) -> List[List[str]]:
    last_available_row_slot = [0] * len(platform[0])

    for i, row in enumerate(platform):
        for j, col in enumerate(row):
            if col == '#':
                last_available_row_slot[j] = i + 1

            elif col == 'O':
                platform[i][j] = '.'
                platform[last_available_row_slot[j]][j] = 'O'
                last_available_row_slot[j] += 1

    return platform


def compute_load_on_north(platform: List[List[str]]) -> int:
    load = 0
    n = len(platform)

    for i, row in enumerate(platform):
        for col in row:
            if col == 'O':
                load += (n - i)
    return load


def run_n_cycles(platform: List[List[str]], n: int = 1) -> List[List[str]]:
    def grid2str(grid: List[List[str]]) -> str:
        return '_'.join(''.join(row) for row in grid)

    def str2grid(string: str) -> List[List[str]]:
        return [[col for col in row] for row in string.split('_')]

    history2order = dict()  # We'll keep a history2order of platforms
    order2history = dict()  # 2-way dict
    start = 0
    period = n + 1

    for i in range(1, n + 1):
        platform = tilt(platform)         # N
        platform = tilt(rotate(platform)) # W
        platform = tilt(rotate(platform)) # S
        platform = tilt(rotate(platform)) # E
        platform = rotate(platform)       # Back to N

        str_platform = grid2str(platform)

        # Cycle detection
        if str_platform in history2order:
            start = history2order[str_platform]
            period = i - start
            break

        history2order[str_platform] = i
        order2history[i] = str_platform

    return str2grid(order2history[start + (n - start) % period])


def main():
    import os
    import sys

    # To be able to import the helpers module
    sys.path.append(os.path.dirname(                                        # Project
                        os.path.dirname(                                    # Year
                            os.path.dirname(os.path.abspath(__file__)))))   # Day

    from helpers import Timer

    with open("input.txt", "r") as file:
        platform = [[char for char in line] for line in file.read().split('\n')]

    # --- Part 1 --- #
    with Timer():
        print("Total load on the north support:", compute_load_on_north(tilt(platform)))  # 105208

    # --- Part 2 --- #
    with Timer():
        print("Total load on the north support after cycles:",
              compute_load_on_north(run_n_cycles(platform, 1_000_000_000)))  # 102943


if __name__ == "__main__":
    main()
