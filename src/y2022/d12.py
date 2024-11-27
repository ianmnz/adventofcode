# Advent of Code : Day 12 - Hill Climbing Algorithm
# https://adventofcode.com/2022/day/12

import heapq
import os
from collections import deque, namedtuple
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

    def __lt__(self, other: "Node") -> bool:
        return (self.pos.real, self.pos.imag) < (other.pos.real, other.pos.imag)


ASearch = namedtuple("ASearch", ["f", "g", "h"])


@Timer.timeit
def build_graph(
    heightmap: List[str],
) -> Tuple[Dict[complex, Node], complex, List[complex]]:
    m, n = len(heightmap), len(heightmap[0])

    def is_valid(x: int, y: int) -> bool:
        return 0 <= x < m and 0 <= y < n

    def height(x: int, y: int) -> int:
        return char_to_int(heightmap[x][y])

    target = 0j
    candidates = []
    nodes = {}
    for i, row in enumerate(heightmap):
        for j, col in enumerate(row):
            node = Node(complex(i, j), char_to_int(col))
            adj = []

            if is_valid(i - 1, j) and height(i - 1, j) <= node.val + 1:
                node.adj.append(complex(i - 1, j))  # Up
                adj.append(heightmap[i - 1][j])

            if is_valid(i + 1, j) and height(i + 1, j) <= node.val + 1:
                node.adj.append(complex(i + 1, j))  # Down
                adj.append(heightmap[i + 1][j])

            if is_valid(i, j - 1) and height(i, j - 1) <= node.val + 1:
                node.adj.append(complex(i, j - 1))  # Left
                adj.append(heightmap[i][j - 1])

            if is_valid(i, j + 1) and height(i, j + 1) <= node.val + 1:
                node.adj.append(complex(i, j + 1))  # Right
                adj.append(heightmap[i][j + 1])

            if col == "S":
                candidates = [node.pos] + candidates
            elif col == "E":
                target = node.pos
            elif (col == "a") and (
                "b" in adj
            ):  # We consider only 'a's that can eventually go uphill
                candidates.append(node.pos)

            nodes[node.pos] = node

    return nodes, target, candidates


def bfs(graph: Dict[complex, Node], start: complex, target: complex) -> int:
    queue: deque[Tuple[int, Node]] = deque([(0, graph[start])])
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
    def manhattan(pos: complex) -> float:
        return abs(pos.real - target.real) + abs(pos.imag - target.imag)

    search_details = {start: ASearch(h := manhattan(start), 0, h)}

    open_list: List[Tuple[float, int, Node]] = [(h, 0, graph[start])]  # (f, g, node)
    closed_list = {key: False for key in graph}

    while open_list:
        _, nb_steps, curr = heapq.heappop(open_list)

        if curr.pos == target:
            return nb_steps

        closed_list[curr.pos] = True

        for adj in curr.adj:
            successor = graph[adj]

            if closed_list[successor.pos]:  # Closed already
                continue

            g = nb_steps + 1
            h = manhattan(successor.pos)
            f = g + h

            if (successor.pos not in search_details) or (
                search_details[successor.pos].f > f
            ):
                heapq.heappush(open_list, (f, g, successor))
                search_details[successor.pos] = ASearch(f, g, h)

    return -1


def dijkstra(graph: Dict[complex, Node], start: complex, target: complex) -> int:
    distances = {}
    distances[start] = 0
    visited = []
    min_curr_dist = float("inf")

    heap: List[Tuple[int, Node]] = [(0, graph[start])]
    while heap:
        nb_steps, curr = heapq.heappop(heap)

        if curr.pos == target:
            min_curr_dist = nb_steps

        visited.append(curr.pos)

        if (
            nb_steps >= min_curr_dist
        ):  # Nb of steps only increase so no need to keep developing this path
            continue

        for adj in curr.adj:
            successor = graph[adj]

            if successor.pos in visited:  # Visited already
                continue

            if (successor.pos not in distances) or (
                distances[successor.pos] > nb_steps + 1
            ):
                heapq.heappush(heap, (nb_steps + 1, successor))
                distances[successor.pos] = nb_steps + 1

    return distances.get(target, -1)


@Timer.timeit
def find_best_path_from_start(
    graph: Dict[complex, Node], target: complex, start: complex
) -> int:
    return bfs(graph, start, target)
    # return A_star_search(graph, start, target)
    # return dijkstra(graph, start, target)


@Timer.timeit
def find_best_start(
    graph: Dict[complex, Node], target: complex, candidates: List[complex]
) -> int:
    return min(
        (
            nb_steps
            for candidate in candidates
            if (nb_steps := bfs(graph, candidate, target)) > 0
            # if (nb_steps := A_star_search(graph, candidate, target)) > 0
            # if (nb_steps := dijkstra(graph, candidate, target)) > 0
        )
    )


@Timer.timeit
def parse(filename: os.PathLike) -> List[str]:
    with open(filename, "r") as file:
        heightmap = file.read().strip().split("\n")
    return heightmap


@Timer.timeit
def solve(filename: os.PathLike) -> Tuple[int, int]:
    heightmap = parse(filename)
    graph, target, candidates = build_graph(heightmap)
    part1 = find_best_path_from_start(graph, target, candidates[0])
    part2 = find_best_start(graph, target, candidates[1:])

    return part1, part2
