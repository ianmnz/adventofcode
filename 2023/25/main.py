# Advent of Code : Day 25 - Snowverload
# https://adventofcode.com/2023/day/25

import collections
import itertools
from typing import List, Dict, Set


def build_graph(network: List[str]) -> Dict[str, Set[str]]:
    graph = collections.defaultdict(set)

    for component in network:
        node, adjacency = component.split(': ')
        adjacency = adjacency.split(' ')

        for adj in adjacency:
            graph[node].add(adj)
            graph[adj].add(node)

    return graph


def iterative_split(graph: Dict[str, Set[str]], cut_value: int = 3) -> int:
    group = set(graph)
    count_adj_in_group = lambda v : len(graph[v] - group)

    while group:
        # Count the number of bridges between both groups
        nb_bridges = sum(map(count_adj_in_group, group))

        if nb_bridges == cut_value:
            break

        # We pass over the component that has more neighbors
        # in the other group
        group.remove(max(group, key=count_adj_in_group))

    return len(group) * len(set(graph) - group)


def minimum_cut(graph: Dict[str, Set[str]], cut_value: int = 3) -> int:
    # Read about and maybe implement the Karger's minimum cut algorithm
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


def solve(filename: str) -> int:
    with open(filename, "r") as file:
        network = [line for line in file.read().split('\n')]

    # return iterative_split(build_graph(network))
    return minimum_cut(build_graph(network))


def main() -> None:
    import os
    from helpers import Timer

    with Timer():
        res = solve(os.path.dirname(os.path.abspath(__file__)) + "/input.txt")

        assert res == 552695, f"Res = {res}"

if __name__ == "__main__":
    main()
