# Advent of Code : Day 21 - Monkey Math
# https://adventofcode.com/2022/day/21

import os
import re
from typing import Dict, Tuple

from helpers import Timer


def expand_ast(root: str, monkeys: Dict[str, str]) -> str:
    pattern = re.compile(r"\w{4}")

    def expand(expr: str) -> str:
        if expr.isnumeric():
            return expr
        else:
            for monkey in pattern.findall(expr):
                expr = expr.replace(monkey, "(" + expand(monkeys[monkey]) + ")")
        return expr

    return expand(root)


@Timer.timeit
def get_number_yelled_by_root(root: str, monkeys: Dict[str, str]) -> int:
    return int(eval(expand_ast(root, monkeys)))


@Timer.timeit
def get_number_to_be_yelled(
    root: str, monkeys: Dict[str, str], you: str = "humn"
) -> int:
    # Based on the idea from https://www.reddit.com/r/adventofcode/comments/zrav4h/comment/j133ko6/
    # Using complex numbers instead of "humn", solving for x becomes:
    # lhs.real + lhs.imag * x = rhs => x = rhs - lhs.real / lhs.imag

    for op in "+-*/":
        root = root.replace(op, "=")
    monkeys[you] = "1j"
    lhs, rhs = map(eval, expand_ast(root, monkeys).split("="))
    return int((rhs - lhs.real) / lhs.imag)


@Timer.timeit
def parse(filename: os.PathLike) -> Dict[str, str]:
    with open(filename, "r") as file:
        lines = file.read().strip().split("\n")

    monkeys = {}
    for line in lines:
        key, value = line.split(": ")
        monkeys[key] = value
    return monkeys


@Timer.timeit
def solve(filename: os.PathLike) -> Tuple[int, int]:
    monkeys = parse(filename)
    part1 = get_number_yelled_by_root(monkeys["root"], monkeys)
    part2 = get_number_to_be_yelled(monkeys["root"], monkeys)

    return part1, part2
