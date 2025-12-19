# Advent of Code : Day 10 - Factory
# https://adventofcode.com/2025/day/10

import re
from collections import deque
from collections.abc import Iterable

import numpy as np
from helpers import Timer, load_input_data
from scipy.optimize import linprog

Machine = tuple[int, list[tuple[int, ...]], tuple[int, ...]]
DIAGRAM_MAP = {"#": "1", ".": "0"}


def bfs(target: int, adjacency: Iterable[int], source: int = 0) -> int:
    q: deque[tuple[int, int]] = deque()
    visited: set[int] = set()

    q.append((0, source))
    while q:
        depth, curr = q.popleft()

        if curr in visited:
            continue

        visited.add(curr)

        for adj in adjacency:
            next = curr ^ adj

            # Early return if target will be reached
            # on next state
            if next == target:
                return depth + 1

            if next not in visited:
                q.append((depth + 1, next))

    return -1


def solve_lp(
    wiring_schematics: Iterable[tuple[int, ...]], joltage_requirements: tuple[int, ...]
) -> int:
    # min cT * x
    # s.t. Ax = b
    # x >= 0
    m, n = len(joltage_requirements), len(wiring_schematics)

    # We want the sum of x
    c = np.ones(n, dtype=int)

    # Fill constraints
    A = np.zeros((m, n), dtype=int)
    for j, col_idx in enumerate(wiring_schematics):
        for i in col_idx:
            A[i][j] = 1

    b = np.array(joltage_requirements)

    # Solve for integer solutions only
    res = linprog(c, A_eq=A, b_eq=b, integrality=1)

    return int(res.fun)


def configure_light_indicators(machines: Iterable[Machine]) -> int:
    # Convert tuple of schematic into bit-masked number
    # (reversed to keep convention!)
    def schematic2bitmask(schematic: list[tuple[int, ...]]) -> list[int]:
        return [sum(1 << exp for exp in indexes) for indexes in schematic]

    return sum(
        bfs(light_diagram, schematic2bitmask(wiring_schematics))
        for light_diagram, wiring_schematics, _ in machines
    )


def configure_joltage_counters(machines: Iterable[Machine]) -> int:
    return sum(
        solve_lp(wiring_schematics, joltage_requirements)
        for _, wiring_schematics, joltage_requirements in machines
    )


def parse_light_diagram(light_diagram: str) -> int:
    # The string is reversed to follow the usual convention:
    # the least-important-bit (index=0) is the rightmost one;
    # the most-important-bit (index=n) is the leftmost one
    return int("".join(map(lambda c: DIAGRAM_MAP[c], light_diagram))[::-1], 2)


def parse_wiring_schematics(wiring_schematics: str) -> list[tuple[int, ...]]:
    return [
        tuple(int(receiver) for receiver in match.split(","))
        for match in re.findall(r"[,\d]+", wiring_schematics)
    ]


def parse_joltage_requirements(joltage_requirements: str) -> tuple[int, ...]:
    return tuple(map(int, joltage_requirements.split(",")))


@Timer.timeit
def parse(data: str) -> list[Machine]:
    machines = []
    pattern = re.compile(
        r"\[(?P<light_diagram>.*)\] (?P<wiring_schematics>\(.*\)+) \{(?P<joltage_requirements>.*)\}"
    )

    for line in data.split("\n"):
        if (matches := pattern.match(line)) is not None:
            light_diagram = parse_light_diagram(matches.group("light_diagram"))
            wiring_schematics = parse_wiring_schematics(
                matches.group("wiring_schematics")
            )
            joltage_requirements = parse_joltage_requirements(
                matches.group("joltage_requirements")
            )
            machines.append((light_diagram, wiring_schematics, joltage_requirements))

    return machines


@Timer.timeit
def solve(data: str) -> tuple[int, int]:
    machines = parse(data)
    part1 = configure_light_indicators(machines)
    part2 = configure_joltage_counters(machines)

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2025, 10)))
