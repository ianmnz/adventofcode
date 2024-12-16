# Advent of Code : Day 16 - Reindeer Maze
# https://adventofcode.com/2024/day/16

from collections import defaultdict
from heapq import heappop, heappush
from typing import TypeAlias

from helpers import Timer, load_input_data

Prev: TypeAlias = dict[tuple[complex, complex], list[tuple[complex, complex]]]


@Timer.timeit
def find_shortest_path(
    source: complex, dir: complex, target: complex, maze: list[list[str]]
) -> tuple[int, Prev]:
    heap = []
    heappush(heap, (0, t := 0, source, dir))
    visited = defaultdict(lambda: float("inf"))
    prev = {(source, dir): []}

    while heap:
        score, _, curr, d = heappop(heap)

        if curr == target:
            return score, prev

        # Forward, clockwise, anti-clockwise
        for dz, cost in (d, 1), (d * -1j, 1001), (d * 1j, 1001):
            z = curr + dz
            c_score = score + cost

            if maze[int(z.real)][int(z.imag)] != "#" and visited[(z, dz)] >= c_score:
                if visited[(z, dz)] > c_score:
                    heappush(heap, (c_score, t := t + 1, z, dz))
                    visited[(z, dz)] = c_score
                    prev[(z, dz)] = []

                prev[(z, dz)].append((curr, d))

    return -1, {}


@Timer.timeit
def backtrack(target: complex, prev: Prev) -> int:
    dir = next(dz for dz in (-1, 1j, 1, -1j) if (target, dz) in prev)
    paths = set()
    curr = {(target, dir)}

    while curr:
        paths |= {pos for pos, _ in curr}
        curr = {aux for node in curr for aux in prev[node]}

    return len(paths)


@Timer.timeit
def find_lowest_score_paths(maze: list[list[str]]) -> tuple[int, int]:
    source = next(
        complex(i, j)
        for i, row in enumerate(maze)
        for j, col in enumerate(row)
        if col == "S"
    )
    target = next(
        complex(i, j)
        for i, row in enumerate(maze)
        for j, col in enumerate(row)
        if col == "E"
    )
    dir = 1j

    score, prev = find_shortest_path(source, dir, target, maze)
    best_nodes_len = backtrack(target, prev)

    return score, best_nodes_len


@Timer.timeit
def parse(data: str) -> list[list[str]]:
    return [[col for col in row] for row in data.splitlines()]


@Timer.timeit
def solve(data: str) -> tuple[int, int]:
    maze = parse(data)
    part1, part2 = find_lowest_score_paths(maze)

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2024, 16)))
