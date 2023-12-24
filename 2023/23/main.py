# Advent of Code : Day 23 - A Long Walk
# https://adventofcode.com/2023/day/23

import collections
import heapq
from typing import List, Dict, Tuple, Callable


def build_graph(carte: List[List[str]], with_slippery_slope = True) -> Tuple[complex, complex, Dict[complex, List[complex]]]:
    n = len(carte)
    m = len(carte[0])

    graph = collections.defaultdict(lambda: set())
    add_neighbor: Callable[[complex, complex, Dict], None] = lambda z, n, G=graph: G[z].add((n, 1))

    for i, row in enumerate(carte[1:n-1], 1):
        for j, col in enumerate(row):
            if col == '#':
                continue

            node = complex(i, j)
            left  = node + ( 0 - 1j)
            right = node + ( 0 + 1j)
            up    = node + (-1 + 0j)
            down  = node + ( 1 + 0j)

            if with_slippery_slope and (col in '<^v>'):
                if col == '>':
                    add_neighbor(node, right)

                elif col == '<':
                    add_neighbor(node, left)

                elif col == 'v':
                    add_neighbor(node, down)

                else: # col == '^'
                    add_neighbor(node, up)
            else:
                # We assume a border of walls to simplify checks
                if carte[i][j + 1] != '#' and ((not with_slippery_slope) or carte[i][j + 1] != '<'):
                    add_neighbor(node, right)

                if carte[i][j - 1] != '#' and ((not with_slippery_slope) or carte[i][j - 1] != '>'):
                    add_neighbor(node, left)

                if carte[i + 1][j] != '#' and ((not with_slippery_slope) or carte[i + 1][j] != '^'):
                    add_neighbor(node, down)

                if carte[i - 1][j] != '#' and ((not with_slippery_slope) or carte[i - 1][j] != 'v'):
                    add_neighbor(node, up)

    source = complex(0, 1)
    target = complex(n - 1, m - 2)

    add_neighbor(source, source + ( 1 + 0j))
    add_neighbor(target, target + (-1 + 0j))

    if not with_slippery_slope:
        while True:
            for node, adjacency in graph.items():
                if len(adjacency) == 2:
                    first, second = adjacency

                    graph[first[0]].remove((node, first[1]))
                    graph[second[0]].remove((node, second[1]))

                    graph[first[0]].add((second[0], first[1] + second[1]))
                    graph[second[0]].add((first[0], first[1] + second[1]))

                    del graph[node]
                    break
            else:
                break

    return source, target, graph


def get_longest_path_length(carte: List[List[str]], with_slippery_slope = True) -> int:
    source, target, graph = build_graph(carte, with_slippery_slope)

    stack = [(source, 0)]
    visited = set()
    longest = 0

    # DFS with back track
    while stack:
        current, distance = stack.pop()

        if distance < 0:
            visited.remove(current)
            continue

        if current == target:
            longest = max(longest, distance)
            continue

        if current in visited:
            continue

        visited.add(current)
        stack.append((current, -1)) # for back tracking

        for neighbor, dist in graph[current]:
            stack.append((neighbor, distance + dist))

    return longest


def main():
    import os
    import sys

    # To be able to import the helpers module
    sys.path.append(os.path.dirname(                                        # Project
                        os.path.dirname(                                    # Year
                            os.path.dirname(os.path.abspath(__file__)))))   # Day

    from helpers import Timer

    with open("input.txt", "r") as file:
        carte = [[char for char in line] for line in file.read().split('\n')]

    # --- Part 1 --- #
    with Timer():
        print("Longest path length:", get_longest_path_length(carte))  # 2246

    # --- Part 2 --- #
    with Timer():
        print("Longest path length without slopes:", get_longest_path_length(carte, False))  #


if __name__ == "__main__":
    main()
