# Advent of Code : Day 09 - Mirage Maintenance
# https://adventofcode.com/2023/day/9

from typing import List


def extrapolate(history: List[int]) -> int:
    deltas = [t - t_1 for t_1, t in zip(history, history[1:])]
    return history[-1] + extrapolate(deltas) if any(t != 0 for t in history) else 0


def main():
    import os
    import sys

    # To be able to import the helpers module
    sys.path.append(os.path.dirname(                                        # Project
                        os.path.dirname(                                    # Year
                            os.path.dirname(os.path.abspath(__file__)))))   # Day

    from helpers import Timer

    with open("input.txt", "r") as file:
        histories = [[*map(int, line.split())] for line in file]

    # --- Part 1 --- #
    with Timer():
        print("Sum of extrapolated histories:", sum([extrapolate(history) for history in histories]))  # 1939607039

    # --- Part 2 --- #
    with Timer():
        print("Sum of backward extrapolated histories:", sum([extrapolate(history[::-1]) for history in histories]))  # 1041


if __name__ == "__main__":
    main()
