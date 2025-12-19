# Advent of Code : Day 01 - Secret Entrance
# https://adventofcode.com/2025/day/1

from collections.abc import Iterable

from helpers import Timer, load_input_data

DIAL_STARTING_POS: int = 50
DIAL_SIZE: int = 100


@Timer.timeit
def parse(data: str) -> Iterable[tuple[int, int]]:
    return [(-1 if turn[0] == "L" else 1, int(turn[1:])) for turn in data.split("\n")]


def turn_dial(turns: Iterable[tuple[int, int]]) -> tuple[int, int]:
    nb_zeros_pos = 0
    nb_zeros_click = 0

    curr_pos = DIAL_STARTING_POS
    for dir, dist in turns:
        prev_pos = curr_pos
        spins, curr_pos = divmod(curr_pos + dir * dist, DIAL_SIZE)

        if dir < 0:  # Compensating when going left:
            # Over-counting: when starting at 0 'spins' will be offset by +1:
            nb_zeros_click -= prev_pos == 0

            # Under-counting: when finishing at 0 'spins' will be offset by -1
            nb_zeros_click += curr_pos == 0

        nb_zeros_pos += curr_pos == 0
        nb_zeros_click += abs(spins)

    return nb_zeros_pos, nb_zeros_click


@Timer.timeit
def solve(data: str) -> tuple[int, int]:
    rotations = parse(data)
    part1, part2 = turn_dial(rotations)

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2025, 1)))
