# Advent of Code : Day 25 - Snowverload
# https://adventofcode.com/2023/day/25

import collections
import functools
import itertools
import os

from helpers import Timer


@Timer.timeit
def build_graph(network: list[str]) -> dict[str, set[str]]:
    graph = collections.defaultdict(set)

    for component in network:
        node, adjacency = component.split(": ")
        adjacency = adjacency.split(" ")

        for adj in adjacency:
            graph[node].add(adj)
            graph[adj].add(node)

    return graph


@Timer.timeit
def iterative_split(graph: dict[str, set[str]], cut_value: int = 3) -> int:
    group = set(graph)

    def count_adj_in_group(v):
        return len(graph[v] - group)

    while group:
        # Count the number of bridges between both groups
        nb_bridges = sum(map(count_adj_in_group, group))

        if nb_bridges == cut_value:
            break

        # We pass over the component that has more neighbors
        # in the other group
        group.remove(max(group, key=count_adj_in_group))

    return len(group) * len(set(graph) - group)


@Timer.timeit
def minimum_cut(graph: dict[str, set[str]], cut_value: int = 3) -> int:
    import networkx as nx

    G = nx.DiGraph()
    for node, adjacency in graph.items():
        for adj in adjacency:
            G.add_edge(node, adj, capacity=1)
            G.add_edge(adj, node, capacity=1)

    for source, target in itertools.combinations(graph, 2):
        cut, (group1, group2) = nx.minimum_cut(G, source, target)

        if cut == cut_value:
            return len(group1) * len(group2)

    return -1


@Timer.timeit
def karger_min_cut(
    graph: dict[str, set[str]], monte_carlo_iterations: int = 200, cut_value: int = 3
) -> int:
    import random

    parent: dict[str, tuple[str, int]]

    def find(v: str) -> tuple[str, int]:
        if parent[v][0] != v:
            parent[v] = find(parent[v][0])
        return parent[v]

    def unite(v: str, u: str) -> None:
        v_group, v_rank = find(v)
        u_group, u_rank = find(u)

        if v_rank < u_rank:
            parent[v_group] = (u_group, v_rank)
        elif v_rank > u_rank:
            parent[u_group] = (v_group, u_rank)
        else:
            parent[u_group] = (v_group, u_rank)
            parent[v_group] = (v_group, v_rank + 1)

    edges = list(
        set(
            [
                (min(node, adj), max(node, adj))
                for node, adjacency in graph.items()
                for adj in adjacency
            ]
        )
    )

    # random.seed(0)
    for _ in range(monte_carlo_iterations):
        parent = {v: (v, 0) for v in graph}
        nb_vertices = len(graph)
        random.shuffle(edges)

        idx = -1
        while nb_vertices > 2:
            idx += 1
            v, u = edges[idx]

            v_group, _ = find(v)
            u_group, _ = find(u)

            if v_group != u_group:
                unite(v_group, u_group)
                nb_vertices -= 1

        cut_edges = 0
        for v, u in edges:
            v_group, _ = find(v)
            u_group, _ = find(u)

            if v_group != u_group:
                cut_edges += 1

                if cut_edges > cut_value:
                    break

        if cut_edges == cut_value:
            counter = collections.Counter([group for group, _ in parent.values()])
            return functools.reduce((lambda a, b: a * b), counter.values())

    return -1


@Timer.timeit
def solve(filename: os.PathLike) -> int:
    with open(filename, "r") as file:
        network = [line for line in file.read().split("\n")]

    # return iterative_split(build_graph(network))
    # return karger_min_cut(build_graph(network))
    return minimum_cut(build_graph(network))
