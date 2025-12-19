# Advent of Code : Day 03 - Lobby
# https://adventofcode.com/2025/day/3

from collections.abc import Iterable
from operator import itemgetter

from helpers import Timer, load_input_data


@Timer.timeit
def parse(data: str) -> Iterable[str]:
    return data.split("\n")


def joltage_output(battery: str, depth: int) -> str:
    if depth == 0:
        return ""

    n = len(battery)

    if n <= depth:
        return battery

    view = battery[: n - (depth - 1)]
    idx, char = max(enumerate(view), key=itemgetter(1))
    return char + joltage_output(battery[idx + 1 :], depth - 1)


def joltage_output_num(battery: Iterable[int], depth: int) -> int:
    if depth == 1:
        return max(battery)

    n = len(battery)

    if n <= depth:
        return sum(10**exp * digit for exp, digit in enumerate(reversed(battery)))

    n = len(battery)
    view = battery[: n - (depth - 1)]
    idx, char = max(enumerate(view), key=itemgetter(1))
    return 10 ** (depth - 1) * char + joltage_output_num(battery[idx + 1 :], depth - 1)


def compute_total_joltage_output(banks: Iterable[str], nb_batteries: int) -> int:
    # return sum(joltage_output_num(list(map(int, bank)), nb_batteries) for bank in banks)
    return sum(int(joltage_output(bank, nb_batteries)) for bank in banks)


@Timer.timeit
def solve(data: str) -> tuple[int, int]:
    banks = parse(data)
    part1 = compute_total_joltage_output(banks, 2)
    part2 = compute_total_joltage_output(banks, 12)

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2025, 3)))
