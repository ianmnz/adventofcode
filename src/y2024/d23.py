# Advent of Code : Day 23 - LAN Party
# https://adventofcode.com/2024/day/23

import itertools
from typing import Iterable, cast

import networkx as nx

from helpers import Timer, load_input_data


@Timer.timeit
def find_k_cliques(G: nx.Graph, k: int, prefix: str) -> int:
    k_cliques = set()
    for clique in nx.find_cliques(G):
        if len(clique) >= k:
            for sub_clique in itertools.combinations(clique, k):
                if any(vertex.startswith(prefix) for vertex in sub_clique):
                    k_cliques.add(tuple(sorted(sub_clique)))
    return len(k_cliques)


@Timer.timeit
def find_max_clique(G: nx.Graph) -> str:
    max_clique, _ = nx.max_weight_clique(G, None)  # type: ignore
    return ",".join(sorted(cast(Iterable, max_clique)))


@Timer.timeit
def parse(data: str) -> nx.Graph:
    G = nx.Graph()
    for edge in data.splitlines():
        lhs, rhs = edge.split("-")
        G.add_edge(lhs, rhs)
    return G


@Timer.timeit
def solve(data: str) -> tuple[int, str]:
    graph = parse(data)
    part1 = find_k_cliques(graph, 3, "t")
    part2 = find_max_clique(graph)

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2024, 23)))
