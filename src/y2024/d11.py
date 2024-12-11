# Advent of Code : Day 11 - Plutonian Pebbles
# https://adventofcode.com/2024/day/11

from functools import cache
from math import floor, log10

from helpers import Timer, load_input_data


@cache
def blink(stone: int, nb_blinks_left: int) -> int:
    if nb_blinks_left == 0:
        return 1

    if stone == 0:
        return blink(1, nb_blinks_left - 1)

    if (size := floor(log10(stone)) + 1) % 2 == 0:
        lhs, rhs = divmod(stone, 10 ** (size // 2))
        return blink(lhs, nb_blinks_left - 1) + blink(rhs, nb_blinks_left - 1)

    return blink(2024 * stone, nb_blinks_left - 1)


@Timer.timeit
def watch_stones(initial_arr: list[int], nb_blinks: int) -> int:
    return sum(blink(stone, nb_blinks) for stone in initial_arr)


@Timer.timeit
def parse(data: str) -> list[int]:
    return list(map(int, data.split()))


@Timer.timeit
def solve(data: str) -> tuple[int, int]:
    stones = parse(data)
    part1 = watch_stones(stones, 25)
    part2 = watch_stones(stones, 75)

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2024, 11)))
