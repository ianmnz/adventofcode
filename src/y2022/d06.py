# Advent of Code : Day 06 - Tuning Trouble
# https://adventofcode.com/2022/day/6

import os
from typing import Tuple

from helpers import Timer

SoP_marker_length = 4  # Start-of-Packet
SoM_marker_length = 14  # Start-of-Message


@Timer.timeit
def find_marker_index(buffer: str, marker_length: int, start: int) -> int:
    for idx in range(start, len(buffer)):
        subbuffer = set(buffer[idx - (marker_length - 1) : idx + 1])

        if len(subbuffer) == marker_length:
            return idx + 1

    return -1


@Timer.timeit
def parse(filename: os.PathLike) -> str:
    with open(filename, "r") as file:
        buffer = file.read().rstrip("\n")
    return buffer


@Timer.timeit
def solve(filename: os.PathLike) -> Tuple[int, int]:
    buffer = parse(filename)
    part1 = find_marker_index(buffer, SoP_marker_length, SoP_marker_length - 1)
    # We assume here that the start-of-message comes after the start-of-packet
    part2 = find_marker_index(buffer, SoM_marker_length, part1)

    return part1, part2
