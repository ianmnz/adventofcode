# Advent of Code : Day 13 - Claw Contraption
# https://adventofcode.com/2024/day/13

import re
from math import floor
from typing import NamedTuple

from helpers import Timer, load_input_data


class Vec2D(NamedTuple):
    x: int
    y: int


def solve_eq_system(
    machine: tuple[Vec2D, Vec2D, Vec2D], factor, cost: Vec2D = Vec2D(3, 1)
) -> int:
    # Ax * x + Bx * y = Px
    # Ay * x + By * y = Py
    #
    # [ Ax  Bx ] * ( x ) = ( Px )
    # [ Ay  By ]   ( y )   ( Py )
    #
    # ( x ) =  1  [  By  -Bx ] * ( Px )
    # ( y )   det [ -Ay   Ax ]   ( Py )

    A, B, P = machine
    P = Vec2D(P.x + factor, P.y + factor)

    det = A.x * B.y - A.y * B.x

    assert det != 0

    x = (P.x * B.y - P.y * B.x) / det
    y = (P.y * A.x - P.x * A.y) / det

    if floor(x) != x or floor(y) != y:
        return 0

    assert x >= 0 and y >= 0

    return int(cost.x * x + cost.y * y)


@Timer.timeit
def get_total_tokens(
    machines: list[tuple[Vec2D, Vec2D, Vec2D]], factor: int = 0
) -> int:
    return sum(solve_eq_system(machine, factor) for machine in machines)


@Timer.timeit
def parse(data: str) -> list[tuple[Vec2D, Vec2D, Vec2D]]:
    machines = []

    patternA = re.compile(r"Button A: X\+(\d+), Y\+(\d+)")
    patternB = re.compile(r"Button B: X\+(\d+), Y\+(\d+)")
    patternP = re.compile(r"Prize: X=(\d+), Y=(\d+)")

    for block in data.split("\n\n"):
        block = block.replace("\n", " ")

        matchA = patternA.search(block)
        matchB = patternB.search(block)
        matchP = patternP.search(block)

        if matchA and matchB and matchP:
            A = Vec2D(int(matchA.group(1)), int(matchA.group(2)))
            B = Vec2D(int(matchB.group(1)), int(matchB.group(2)))
            P = Vec2D(int(matchP.group(1)), int(matchP.group(2)))

            machines.append((A, B, P))

    return machines


@Timer.timeit
def solve(data: str) -> tuple[int, int]:
    machines = parse(data)
    part1 = get_total_tokens(machines)
    part2 = get_total_tokens(machines, 10_000_000_000_000)

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2024, 13)))
