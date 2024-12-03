# Advent of Code : Day 03 - Mull It Over
# https://adventofcode.com/2024/day/03

import os
import re

from helpers import Timer


@Timer.timeit
def compute_mul(memory: str, with_conditional: bool) -> int:
    if with_conditional:
        memory = re.sub(r"don't\(\)(.*?)do\(\)", "", memory.replace("\n", " ") + "do()")
    return sum(int(a) * int(b) for a, b in re.findall(r"mul\((\d+),(\d+)\)", memory))


@Timer.timeit
def parse(filename: os.PathLike) -> str:
    with open(filename, "r") as file:
        memory = file.read()
    return memory


@Timer.timeit
def solve(filename: os.PathLike) -> tuple[int, int]:
    memory = parse(filename)
    part1 = compute_mul(memory, False)
    part2 = compute_mul(memory, True)

    return part1, part2


if __name__ == "__main__":
    from pathlib import Path

    print(solve(Path(__file__).parents[2] / "data" / "2024" / "03.txt"))
