# Advent of Code : Day 01 - Trebuchet?!
# https://adventofcode.com/2023/day/1

import os
import re

from helpers import Timer


@Timer.timeit
def calibrate(document: list[str]) -> int:
    matches = [[digit for digit in re.findall(r"\d", line)] for line in document]

    return sum(int(digits[0] + digits[-1]) for digits in matches)


@Timer.timeit
def fix(document: list[str]) -> list[str]:
    """
    The idea here is to replace the spelled digits
    by their numerical counterparts but keeping the
    first and last characters so it will be able to
    properly replace them.

    An example, a 'twone' would become:
        twone -> t2one -> t2o1e => 21
    And not:
        twone -> 2ne => 2
    """
    return [
        line.replace("one", "o1e")  # or .replace("one", "one1one")
        .replace("two", "t2o")  # or .replace("two", "two2two")
        .replace("three", "t3e")  # or .replace("three", "three3three")
        .replace("four", "f4r")  # or .replace("four", "four4four")
        .replace("five", "f5e")  # or .replace("five", "five5five")
        .replace("six", "s6x")  # or .replace("six", "six6six")
        .replace("seven", "s7n")  # or .replace("seven", "seven7seven")
        .replace("eight", "e8t")  # or .replace("eight", "eight8eight")
        .replace("nine", "n9e")  # or .replace("nine", "nine9nine")
        for line in document
    ]


@Timer.timeit
def parse(filename: os.PathLike) -> list[str]:
    with open(filename, "r") as file:
        document = file.read().strip().split("\n")
    return document


@Timer.timeit
def solve(filename: os.PathLike) -> tuple[int, int]:
    document = parse(filename)
    part1 = calibrate(document)
    part2 = calibrate(fix(document))

    return part1, part2
