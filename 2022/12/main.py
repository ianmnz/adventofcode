# Advent of Code : Day 12 - Hill Climbing Algorithm
# https://adventofcode.com/2022/day/12


from collections import deque
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

from helpers import Timer


def char_to_int(item: str) -> int:
    d = {
        "S": 1,
        "a": 1,
        "b": 2,
        "c": 3,
        "d": 4,
        "e": 5,
        "f": 6,
        "g": 7,
        "h": 8,
        "i": 9,
        "j": 10,
        "k": 11,
        "l": 12,
        "m": 13,
        "n": 14,
        "o": 15,
        "p": 16,
        "q": 17,
        "r": 18,
        "s": 19,
        "t": 20,
        "u": 21,
        "v": 22,
        "w": 23,
        "x": 24,
        "y": 25,
        "z": 26,
        "E": 26,
    }
    return d[item]


@dataclass
class Node:
    pos: complex
    val: int
    adj: List[complex] = field(init=False, default_factory=list)


@Timer.timeit
def build_graph(
    heightmap: List[str],
) -> Tuple[Dict[complex, Node], complex, complex, List[complex]]:
    m, n = len(heightmap), len(heightmap[0])

    is_valid = lambda x, y: (0 <= x < m) and (0 <= y < n)
    height = lambda x, y: char_to_int(heightmap[x][y])

    start = 0j
    target = 0j
    candidates = []
    nodes = {}
    for i, row in enumerate(heightmap):
        for j, col in enumerate(row):
            node = Node(complex(i, j), char_to_int(col))

            if col == "S":
                start = node.pos
            elif col == "E":
                target = node.pos
            elif col == "a":
                candidates.append(node.pos)

            if is_valid(i - 1, j) and height(i - 1, j) <= node.val + 1:
                node.adj.append(complex(i - 1, j))  # Up

            if is_valid(i + 1, j) and height(i + 1, j) <= node.val + 1:
                node.adj.append(complex(i + 1, j))  # Down

            if is_valid(i, j - 1) and height(i, j - 1) <= node.val + 1:
                node.adj.append(complex(i, j - 1))  # Left

            if is_valid(i, j + 1) and height(i, j + 1) <= node.val + 1:
                node.adj.append(complex(i, j + 1))  # Right

            nodes[node.pos] = node

    return nodes, target, start, candidates


def bfs(graph: Dict[complex, Node], start: complex, target: complex) -> int:
    queue = deque([(0, graph[start])])
    visited = {start}

    while queue:
        nb_steps, curr = queue.popleft()

        if curr.pos == target:
            return nb_steps

        for adj in curr.adj:
            successor = graph[adj]

            if successor.pos in visited:  # Visited already
                continue

            visited.add(successor.pos)
            queue.append((nb_steps + 1, successor))

    return -1


def A_star_search(graph: Dict[complex, Node], start: complex, target: complex) -> int:
    ...


@Timer.timeit
def find_best_path_from_start(
    graph: Dict[complex, Node], target: complex, start: complex
) -> int:
    return bfs(graph, start, target)


@Timer.timeit
def find_best_start(
    graph: Dict[complex, Node], target: complex, candidates: List[complex]
) -> int:
    return min(
        (
            nb_steps
            for candidate in candidates
            if (nb_steps := bfs(graph, candidate, target)) > 0
        )
    )


@Timer.timeit
def parse(filename: str) -> List[Tuple[str, int]]:
    with open(filename, "r") as file:
        heightmap = file.read().strip().split("\n")
    return heightmap


@Timer.timeit
def solve(filename: str) -> Tuple[int, int]:
    heightmap = parse(filename)
    graph, target, start, candidates = build_graph(heightmap)
    part1 = find_best_path_from_start(graph, target, start)
    part2 = find_best_start(graph, target, candidates)

    return part1, part2


def main() -> None:
    import os

    res = solve(os.path.dirname(os.path.abspath(__file__)) + "/input.txt")

    assert res[0] == 517, f"Part1 = {res[0]}"
    assert res[1] == 512, f"Part2 = {res[1]}"


if __name__ == "__main__":
    main()
