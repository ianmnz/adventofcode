# Advent of Code : Day 03 - Mull It Over
# https://adventofcode.com/2024/day/03

import re

from helpers import Timer, load_input_data


@Timer.timeit
def compute_mul(memory: str, with_conditional: bool) -> int:
    if with_conditional:
        memory = re.sub(r"don't\(\)(.*?)do\(\)", "", memory.replace("\n", " ") + "do()")
    return sum(int(a) * int(b) for a, b in re.findall(r"mul\((\d+),(\d+)\)", memory))


@Timer.timeit
def parse(data: str) -> str:
    return data


@Timer.timeit
def solve(data: str) -> tuple[int, int]:
    memory = parse(data)
    part1 = compute_mul(memory, False)
    part2 = compute_mul(memory, True)

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2024, 3)))
