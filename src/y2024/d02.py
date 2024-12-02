# Advent of Code : Day 02 - Red-Nosed Reports
# https://adventofcode.com/2024/day/02

import os

from helpers import Timer

DELTA_LOWER: int = 1
DELTA_UPPER: int = 3


def is_increasing(report: list[int]) -> bool:
    return all(
        prev + DELTA_LOWER <= curr <= prev + DELTA_UPPER
        for prev, curr in zip(report[:-1], report[1:])
    )


def is_decreasing(report: list[int]) -> bool:
    return all(
        prev - DELTA_LOWER >= curr >= prev - DELTA_UPPER
        for prev, curr in zip(report[:-1], report[1:])
    )


def check_safety(report: list[int]) -> bool:
    return is_increasing(report) or is_decreasing(report)


def check_safety_with_dampener(report: list[int]) -> bool:
    if check_safety(report):
        return True
    return any(check_safety(report[:i] + report[i + 1 :]) for i in range(len(report)))


@Timer.timeit
def count_nb_safe_reports(reports: list[list[int]], with_dampener: bool) -> int:
    if with_dampener:
        return sum(check_safety_with_dampener(report) for report in reports)
    return sum(check_safety(report) for report in reports)


@Timer.timeit
def parse(filename: os.PathLike) -> list[list[int]]:
    with open(filename, "r") as file:
        reports = [list(map(int, x.split())) for x in file.read().splitlines()]

    return reports


@Timer.timeit
def solve(filename: os.PathLike) -> tuple[int, int]:
    reports = parse(filename)
    part1 = count_nb_safe_reports(reports, False)
    part2 = count_nb_safe_reports(reports, True)

    return part1, part2
