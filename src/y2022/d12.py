# Advent of Code : Day 12 - Hill Climbing Algorithm
# https://adventofcode.com/2022/day/12

import heapq
from collections import deque, namedtuple
from dataclasses import dataclass, field
from typing import Self

from helpers import Timer, load_input_data


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
    adj: list[complex] = field(init=False, default_factory=list)

    def __lt__(self, other: Self) -> bool:
        return (self.pos.real, self.pos.imag) < (other.pos.real, other.pos.imag)


ASearch = namedtuple("ASearch", ["f", "g", "h"])


@Timer.timeit
def build_graph(
    heightmap: list[str],
) -> tuple[dict[complex, Node], complex, list[complex]]:
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


def bfs(graph: dict[complex, Node], start: complex, target: complex) -> int:
    queue: deque[tuple[int, Node]] = deque([(0, graph[start])])
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


def A_star_search(graph: dict[complex, Node], start: complex, target: complex) -> int:
    def manhattan(pos: complex) -> float:
        return abs(pos.real - target.real) + abs(pos.imag - target.imag)

    search_details = {start: ASearch(h := manhattan(start), 0, h)}

    open_list: list[tuple[float, int, Node]] = [(h, 0, graph[start])]  # (f, g, node)
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


def dijkstra(graph: dict[complex, Node], start: complex, target: complex) -> int:
    distances = {}
    distances[start] = 0
    visited = []
    min_curr_dist = float("inf")

    heap: list[tuple[int, Node]] = [(0, graph[start])]
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
    graph: dict[complex, Node], target: complex, start: complex
) -> int:
    return bfs(graph, start, target)
    # return A_star_search(graph, start, target)
    # return dijkstra(graph, start, target)


@Timer.timeit
def find_best_start(
    graph: dict[complex, Node], target: complex, candidates: list[complex]
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
def parse(data: str) -> list[str]:
    return data.strip().split("\n")


@Timer.timeit
def solve(data: str) -> tuple[int, int]:
    heightmap = parse(data)
    graph, target, candidates = build_graph(heightmap)
    part1 = find_best_path_from_start(graph, target, candidates[0])
    part2 = find_best_start(graph, target, candidates[1:])

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2022, 12)))
