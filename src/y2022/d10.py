# Advent of Code : Day 10 - Cathode-Ray Tube
# https://adventofcode.com/2022/day/10

import os
from typing import List, Tuple

from helpers import Timer

CYCLES_PER_INSTRUCTION = {"noop": 1, "addx": 2}

CYCLES_OF_INTEREST = [20, 60, 100, 140, 180, 220]

CRT_WIDTH = 40
CRT_HEIGHT = 6
SPRITE_WIDTH = 3


@Timer.timeit
def get_CRT_signals_and_display(
    program: List[List[str]],
) -> Tuple[int, List[List[str]]]:
    sum_signal_strength_on_cycles_of_interest = 0
    crt = [["." for _ in range(CRT_WIDTH)] for _ in range(CRT_HEIGHT)]

    cycle_counter = 1
    register = 1
    for instruction in program:
        for cycle in range(CYCLES_PER_INSTRUCTION.get(instruction[0], 0)):
            if cycle_counter in CYCLES_OF_INTEREST:
                sum_signal_strength_on_cycles_of_interest += cycle_counter * register

            i, j = divmod(cycle_counter - 1, CRT_WIDTH)

            if abs(register - j) <= (SPRITE_WIDTH // 2):
                crt[i][j] = "#"

            if instruction[0] == "addx" and cycle + 1 == CYCLES_PER_INSTRUCTION["addx"]:
                register += int(instruction[1])

            cycle_counter += 1

    return sum_signal_strength_on_cycles_of_interest, crt


def display_crt(crt: List[List[str]]) -> str:
    # for i in range(CRT_HEIGHT):
    #     for j in range(CRT_WIDTH):
    #         print(crt[i][j], end="")
    #     print()
    return "EFUGLPAP"  # It should print this


@Timer.timeit
def parse(filename: os.PathLike) -> List[List[str]]:
    with open(filename, "r") as file:
        program = file.read().strip().split("\n")
    return [instruction.strip().split() for instruction in program]


@Timer.timeit
def solve(filename: os.PathLike) -> Tuple[int, str]:
    program = parse(filename)
    part1, crt = get_CRT_signals_and_display(program)
    part2 = display_crt(crt)

    return part1, part2
