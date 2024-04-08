# Advent of Code : Day 25 - Full of Hot Air
# https://adventofcode.com/2022/day/25

from typing import List

from helpers import Timer

BASE5: List[int] = []


def snafu2decimal(number_snafu: str) -> int:
    convert = {
        "-": -1,
        "=": -2,
        "0": 0,
        "1": 1,
        "2": 2,
    }
    return sum(
        BASE5[i] * convert[digit_snafu]
        for i, digit_snafu in enumerate(reversed(number_snafu))
    )


@Timer.timeit
def decimal2snafu(number_10: int) -> str:
    convert = {
        -2: "=",
        -1: "-",
        0: "0",
        1: "1",
        2: "2",
    }

    snafu = ""
    q = number_10
    while q:
        q, r = divmod(q, 5)

        if r >= 3:
            # The "carry the one" for r = (3 | 4) ~ (-2 | -1) comes here :
            # it's based on the fact that
            # D = d * q + r =>
            # D = d * q + r (- d + d) =>
            # D = d * (q + 1) + (r - d)
            q += 1
            r -= 5

        snafu += convert[r]

    return snafu[::-1]


@Timer.timeit
def get_total_sum(numbers: List[str]) -> str:
    total_10 = sum(snafu2decimal(number) for number in numbers)
    return decimal2snafu(total_10)


@Timer.timeit
def parse(filename: str) -> List[str]:
    with open(filename, "r") as file:
        numbers = file.read().strip().split("\n")

    global BASE5
    max_power = max(len(number) for number in numbers)
    BASE5 = [pow(5, i) for i in range(max_power)]

    return numbers


@Timer.timeit
def solve(filename: str) -> str:
    numbers = parse(filename)
    part1 = get_total_sum(numbers)

    return part1


def main() -> None:
    import os

    res = solve(os.path.dirname(os.path.abspath(__file__)) + "/input.txt")

    assert res == "2-0-020-1==1021=--01", f"Part1 = {res[0]}"


if __name__ == "__main__":
    main()
