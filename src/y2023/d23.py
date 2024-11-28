# Advent of Code : Day 23 - A Long Walk
# https://adventofcode.com/2023/day/23

import collections
import os
from typing import Callable, Dict

from helpers import Timer


@Timer.timeit
def build_graph(
    carte: list[list[str]], with_slippery_slope=True
) -> tuple[complex, complex, dict[complex, set[tuple[complex, int]]]]:
    n = len(carte)
    m = len(carte[0])

    graph = collections.defaultdict(lambda: set())
    add_neighbor: Callable[[complex, complex, Dict], None] = lambda z, n, G=graph: G[
        z
    ].add((n, 1))

    source = complex(0, 1)
    target = complex(n - 1, m - 2)

    add_neighbor(source, source + (1 + 0j))
    add_neighbor(target, target + (-1 + 0j))

    for i, row in enumerate(carte[1 : n - 1], 1):
        for j, col in enumerate(row):
            if col == "#":
                continue

            node = complex(i, j)
            left = node + (0 - 1j)
            right = node + (0 + 1j)
            up = node + (-1 + 0j)
            down = node + (1 + 0j)

            if with_slippery_slope and (col in "<^v>"):
                if col == ">":
                    add_neighbor(node, right)

                elif col == "<":
                    add_neighbor(node, left)

                elif col == "v":
                    add_neighbor(node, down)

                else:  # col == '^'
                    add_neighbor(node, up)
            else:
                # We assume a border of walls to simplify checks
                if carte[i][j + 1] != "#" and (
                    (not with_slippery_slope) or carte[i][j + 1] != "<"
                ):
                    add_neighbor(node, right)

                if carte[i][j - 1] != "#" and (
                    (not with_slippery_slope) or carte[i][j - 1] != ">"
                ):
                    add_neighbor(node, left)

                if carte[i + 1][j] != "#" and (
                    (not with_slippery_slope) or carte[i + 1][j] != "^"
                ):
                    add_neighbor(node, down)

                if carte[i - 1][j] != "#" and (
                    (not with_slippery_slope) or carte[i - 1][j] != "v"
                ):
                    add_neighbor(node, up)

    # Collapse nodes with only 2 neighbors for performance
    for node, adjacency in graph.items():
        if len(adjacency) == 2:
            (first, weight_f), (second, weight_s) = adjacency

            if ((node, weight_f) not in graph[first]) or (
                (node, weight_s) not in graph[second]
            ):
                continue

            graph[first].remove((node, weight_f))
            graph[second].remove((node, weight_s))

            graph[first].add((second, weight_f + weight_s))
            graph[second].add((first, weight_f + weight_s))

            graph[node] = set()

    return source, target, graph


@Timer.timeit
def get_longest_path_length(carte: list[list[str]], with_slippery_slope=True) -> int:
    source, target, graph = build_graph(carte, with_slippery_slope)

    stack: list[tuple[complex, int]] = [(source, 0)]
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
        stack.append((current, -1))  # for back tracking

        for neighbor, dist in graph[current]:
            stack.append((neighbor, distance + dist))

    return longest


@Timer.timeit
def parse(filename: os.PathLike) -> list[list[str]]:
    with open(filename, "r") as file:
        carte = [[char for char in line] for line in file.read().split("\n")]
    return carte


@Timer.timeit
def solve(filename: os.PathLike) -> tuple[int, int]:
    carte = parse(filename)
    part1 = get_longest_path_length(carte)
    part2 = get_longest_path_length(carte, False)

    return part1, part2
