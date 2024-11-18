# Advent of Code : Day 17 - Clumsy Crucible
# https://adventofcode.com/2023/day/17

import os
from heapq import heappop, heappush
from typing import Dict, List, Tuple

from helpers import Timer


@Timer.timeit
def build_graph(heatmap: List[List[int]]) -> Dict[Tuple[int], int]:
    return {(i, j): col for i, row in enumerate(heatmap) for j, col in enumerate(row)}


@Timer.timeit
def find_shortest_path(graph: Dict[Tuple[int], int], lower: int, upper: int) -> int:
    source = (0, 0)
    dest = [*graph][-1]

    heap = [(0, *source, 1, 0), (0, *source, 0, 1)]
    visited = set()

    while heap:
        cost, px, py, dx, dy = heappop(heap)

        if (px, py) == dest:
            return cost

        if (px, py, dx, dy) in visited:
            continue

        visited.add((px, py, dx, dy))

        for rx, ry in [(dy, -dx), (-dy, dx)]:  # rotate -pi/2, +pi/2
            x, y, c = px, py, cost
            for step in range(1, upper + 1):
                x += rx
                y += ry

                if (x, y) in graph:
                    c += graph[(x, y)]
                    if step >= lower:
                        heappush(heap, (c, x, y, rx, ry))
                else:
                    break
    return -1


@Timer.timeit
def parse(filename: os.PathLike) -> List[List[int]]:
    with open(filename, "r") as file:
        heatmap = [
            [int(heatloss) for heatloss in line] for line in file.read().split("\n")
        ]
    return heatmap


@Timer.timeit
def solve(filename: os.PathLike) -> Tuple[int, int]:
    heatmap = parse(filename)
    graph = build_graph(heatmap)
    part1 = find_shortest_path(graph, 1, 3)
    part2 = find_shortest_path(graph, 4, 10)

    return part1, part2


def main():
    from pathlib import Path

    res = solve(Path(__file__).parent / "input.txt")

    assert res[0] == 674, f"Part1 = {res[0]}"
    assert res[1] == 773, f"Part2 = {res[1]}"


if __name__ == "__main__":
    main()
