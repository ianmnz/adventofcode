# Advent of Code : Day 13 - Claw Contraption
# https://adventofcode.com/2024/day/13

import re
from math import floor
from typing import NamedTuple

from helpers import Timer, load_input_data

COST_A = 3
COST_B = 1


class Point(NamedTuple):
    x: int
    y: int


def solve_eq_system(machine: tuple[Point, Point, Point], factor) -> int:
    # Ax * alpha + Bx * beta = Px
    # Ay * alpha + By * beta = Py
    #
    # [ Ax  Bx ] * ( alpha ) = ( Px )
    # [ Ay  By ]   (  beta )   ( Py )
    #
    # ( alpha ) =  1  [  By  -Bx ] * ( Px )
    # (  beta )   det [ -Ay   Ax ]   ( Py )

    A, B, P = machine
    P = Point(P.x + factor, P.y + factor)

    det = A.x * B.y - A.y * B.x

    assert det != 0

    alpha = (P.x * B.y - P.y * B.x) / det
    beta = (P.y * A.x - P.x * A.y) / det

    if floor(alpha) != alpha or floor(beta) != beta:
        return 0

    assert alpha >= 0 and beta >= 0

    return int(COST_A * alpha + COST_B * beta)


@Timer.timeit
def get_total_tokens(machines: list[tuple[Point, Point, Point]], factor=0) -> int:
    return sum(solve_eq_system(machine, factor) for machine in machines)


@Timer.timeit
def parse(data: str) -> list[tuple[Point, Point, Point]]:
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
            A = Point(int(matchA.group(1)), int(matchA.group(2)))
            B = Point(int(matchB.group(1)), int(matchB.group(2)))
            P = Point(int(matchP.group(1)), int(matchP.group(2)))

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
