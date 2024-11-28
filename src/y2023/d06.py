# Advent of Code : Day 06 - Wait For It
# https://adventofcode.com/2023/day/6

import math
import os

from helpers import Timer


@Timer.timeit
def calculate_margin_of_error(times: list[int], records: list[int]) -> int:
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
        # Small perturbation to avoid integers
        h_left = math.ceil((time - sqrt) / 2 + 0.1)
        h_right = math.floor((time + sqrt) / 2 - 0.1)

        nb_of_ways_to_beat_record *= h_right - h_left + 1

    return nb_of_ways_to_beat_record


@Timer.timeit
def parse(filename: os.PathLike) -> tuple[list[int], list[int]]:
    with open(filename, "r") as file:
        times, record_distances = map(
            lambda ss: list(map(int, ss.split()[1:])), file.read().split("\n")
        )
    return times, record_distances


@Timer.timeit
def solve(filename: os.PathLike) -> tuple[int, int]:
    times, record_distances = parse(filename)

    part1 = calculate_margin_of_error(times, record_distances)

    times = [int("".join(map(str, times)))]
    record_distances = [int("".join(map(str, record_distances)))]

    part2 = calculate_margin_of_error(times, record_distances)

    return part1, part2
