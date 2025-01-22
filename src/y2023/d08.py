# Advent of Code : Day 08 - Haunted Wasteland
# https://adventofcode.com/2023/day/8

import math
import re

from helpers import Timer, load_input_data


@Timer.timeit
def build_graph(nodes: list[str]) -> dict[str, dict[str, str]]:
    graph = dict()
    pattern = re.compile(r"(\w{3}) = \((\w{3}), (\w{3})\)")

    for node in nodes:
        match = pattern.match(node)

        if match is None:
            continue

        graph[match.group(1)] = {"L": match.group(2), "R": match.group(3)}

    return graph


def follow_sequence(sequence: str, start: str, graph: dict[str, dict[str, str]]) -> str:
    curr = start
    for instruction in sequence:
        curr = graph[curr][instruction]
    return curr


@Timer.timeit
def count_steps_to_exit(sequence: str, nodes: list[str]) -> int:
    graph = build_graph(nodes)
    curr = "AAA"

    nb_cycles = 0
    while curr != "ZZZ":
        curr = follow_sequence(sequence, curr, graph)
        nb_cycles += 1

    return nb_cycles * len(sequence)


@Timer.timeit
def count_simultaneous_steps_to_exit(sequence: str, nodes: list[str]) -> int:
    graph = build_graph(nodes)

    curs = []
    ends = []
    for node in graph.keys():
        if node.endswith("A"):
            curs.append(node)

        elif node.endswith("Z"):
            ends.append(node)

    nb_cycles_by_start = []
    for curr in curs:
        nb_cycles = 0
        while curr not in ends:
            curr = follow_sequence(sequence, curr, graph)
            nb_cycles += 1

        nb_cycles_by_start.append(nb_cycles)

    def lcm(numbers: list[int]) -> int:
        prod = numbers[0]
        for number in numbers[1:]:
            prod = (prod * number) // math.gcd(prod, number)
        return prod

    return len(sequence) * lcm(nb_cycles_by_start)


@Timer.timeit
def parse(data: str) -> tuple[str, str]:
    sequence, nodes = data.strip().split("\n\n")
    return sequence, nodes


@Timer.timeit
def solve(data: str) -> tuple[int, int]:
    sequence, nodes = parse(data)
    part1 = count_steps_to_exit(sequence.strip(), nodes.split("\n"))
    part2 = count_simultaneous_steps_to_exit(sequence.strip(), nodes.split("\n"))

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2023, 8)))
