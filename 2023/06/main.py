# Advent of Code : Day 06 - Wait For It
# https://adventofcode.com/2023/day/6

import math
from typing import List


def calculate_margin_of_error(times: List[int], records: List[int]) -> int:
    nb_of_ways_to_beat_record = 1

    for time, record in zip(times, records):
        """
        Since the function f(h) = h * (t - h) represents the distance
        Using the quadratic equation solution to define the values which
        the distance equals the record, we find that
            f(h) = h * (t - h) > record =>
            -h**2 + h*t - record > 0 =>
            (t - sqrt(t**2 - 4 * record))/2 < h_solve < (t + sqrt(t**2 - 4 * record))/2
        """
        delta = (time * time) - 4 * record
        if delta < 0:
            return 0

        sqrt = math.sqrt(delta)
        h_left = math.ceil((time - sqrt)/2 + 0.1)   # Small perturbation to avoid integers
        h_right = math.floor((time + sqrt)/2 - 0.1)

        nb_of_ways_to_beat_record *= (h_right - h_left + 1)

    return nb_of_ways_to_beat_record


def main():
    import os
    import sys

    # To be able to import the helpers module
    sys.path.append(os.path.dirname(                                        # Project
                        os.path.dirname(                                    # Year
                            os.path.dirname(os.path.abspath(__file__)))))   # Day

    from helpers import Timer

    with open("input.txt", "r") as file:
        times, record_distances = map(lambda ss: list(map(int, ss.split()[1:])), file.read().split('\n'))

    # --- Part 1 --- #
    with Timer():
        print("Margin of error:", calculate_margin_of_error(times, record_distances))  # 316800

    # --- Part 2 --- #
    times = [int(''.join(map(str, times)))]
    record_distances = [int(''.join(map(str, record_distances)))]
    with Timer():
        print("Margin of error with kerning:", calculate_margin_of_error(times, record_distances))  # 45647654


if __name__ == "__main__":
    main()
