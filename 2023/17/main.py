# Advent of Code : Day 17 - Clumsy Crucible
# https://adventofcode.com/2023/day/17

from typing import List, Dict, Tuple
from heapq import heappush, heappop


def build_graph(heatmap: List[List[int]]) -> Dict[Tuple[int], int]:
    return {(i, j): col
            for i, row in enumerate(heatmap)
            for j, col in enumerate(row)}


def find_shortest_path(graph: Dict[Tuple[int], int], lower: int, upper: int) -> int:

    source = (0, 0)
    dest = [*graph][-1]

    heap = [(0, *source, 1, 0), (0, *source, 0, 1)]
    visited = set()

    while heap:
        cost, px, py, dx, dy = heappop(heap)

        if ((px, py) == dest):
            return cost

        if (px, py, dx, dy) in visited:
            continue

        visited.add((px, py, dx, dy))

        for rx, ry in [(dy, -dx), (-dy, dx)]: # rotate -pi/2, +pi/2
            x, y, c = px, py, cost
            for step in range(1, upper+1):
                x += rx
                y += ry

                if (x, y) in graph:
                    c += graph[(x, y)]
                    if step >= lower:
                        heappush(heap, (c, x, y, rx, ry))
                else:
                    break
    return -1


def main():
    import os
    import sys

    # To be able to import the helpers module
    sys.path.append(os.path.dirname(                                        # Project
                        os.path.dirname(                                    # Year
                            os.path.dirname(os.path.abspath(__file__)))))   # Day

    from helpers import Timer

    with open("input.txt", "r") as file:
        heatmap = [[int(heatloss) for heatloss in line] for line in file.read().split('\n')]

    # --- Part 1 --- #
    with Timer():
        print("Least heat loss:", find_shortest_path(build_graph(heatmap), 1, 3))  # 674

    # --- Part 2 --- #
    with Timer():
        print("Least heat loss for ultra:", find_shortest_path(build_graph(heatmap), 4, 10))  # 773


if __name__ == "__main__":
    main()
