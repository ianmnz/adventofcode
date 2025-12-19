# Advent of Code : Day 11 - Reactor
# https://adventofcode.com/2025/day/11

from collections import defaultdict, deque

from helpers import Timer, load_input_data

Graph = dict[str, list[str]]


def get_nb_paths(graph: Graph, s: str, t: str) -> int:
    # Simple DFS with counting instead of returning
    res = 0
    stack = [s]
    while stack:
        vertex = stack.pop()

        if vertex == t:
            res += 1
            continue

        stack.extend(graph[vertex])

    return res


def topological_sort(graph: Graph) -> list[str]:
    in_degree = defaultdict(int)
    for u in graph:
        for v in graph[u]:
            in_degree[v] += 1

    queue = deque((u for u in graph if in_degree[u] == 0))
    order = []

    while queue:
        u = queue.popleft()
        order.append(u)

        for v in graph.get(u, []):
            in_degree[v] -= 1
            if not in_degree[v]:
                queue.append(v)

    return order


def get_nb_paths_with_stops(graph: Graph, s: str, t: str, stops: set[str]) -> int:
    stop_idx = {u: i for i, u in enumerate(stops)}
    full_mask = (1 << len(stops)) - 1

    topo = topological_sort(graph)
    dp = defaultdict(lambda: defaultdict(int))

    initial_mask = 0
    if s in stops:
        initial_mask |= 1 << stop_idx[s]
    dp[s][initial_mask] = 1

    for u in topo:
        for mask, count in dp[u].items():
            for v in graph.get(u, []):
                next_mask = mask
                if v in stop_idx:
                    next_mask |= 1 << stop_idx[v]
                dp[v][next_mask] += count

    return dp[t][full_mask]


@Timer.timeit
def parse(data: str) -> Graph:
    graph = {}
    for row in data.split("\n"):
        key, values = row.split(":")
        graph[key] = values.split()
    return graph


@Timer.timeit
def solve(data: str) -> tuple[int, int]:
    graph = parse(data)
    part1 = get_nb_paths(graph, "you", "out")
    part2 = get_nb_paths_with_stops(graph, "svr", "out", {"fft", "dac"})

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2025, 11)))
