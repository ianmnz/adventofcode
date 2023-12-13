# Advent of Code : Day 08 - Haunted Wasteland
# https://adventofcode.com/2023/day/8

import re
import math
from typing import List, Dict


def build_graph(nodes: List[str]) -> Dict[str, Dict[str, str]]:
    graph = dict()
    pattern = re.compile(r'(\w{3}) = \((\w{3}), (\w{3})\)')

    for node in nodes:
        match = pattern.match(node)
        graph[match.group(1)] = {'L': match.group(2),
                                 'R': match.group(3)}

    return graph


def follow_sequence(sequence: str, start: str, graph: Dict[str, Dict[str, str]]) -> str:
    curr = start
    for instruction in sequence:
        curr = graph[curr][instruction]
    return curr


def count_steps_to_exit(sequence: str, nodes: List[str]) -> int:
    graph = build_graph(nodes)
    curr = 'AAA'

    nb_cycles = 0
    while curr != 'ZZZ':
        curr = follow_sequence(sequence, curr, graph)
        nb_cycles += 1

    return nb_cycles * len(sequence)


def count_simultaneous_steps_to_exit(sequence: str, nodes: List[str]) -> int:
    graph = build_graph(nodes)

    curs = []
    ends = []
    for node in graph.keys():
        if node.endswith('A'):
            curs.append(node)

        elif node.endswith('Z'):
            ends.append(node)

    nb_cycles_by_start = []
    for curr in curs:
        nb_cycles = 0
        while (curr not in ends):
            curr = follow_sequence(sequence, curr, graph)
            nb_cycles += 1

        nb_cycles_by_start.append(nb_cycles)

    def lcm(numbers: List[int]) -> int:
        prod = numbers[0]
        for number in numbers[1:]:
            prod = (prod * number) // math.gcd(prod, number)
        return prod

    return len(sequence) * lcm(nb_cycles_by_start)


def main():
    import os
    import sys

    # To be able to import the helpers module
    sys.path.append(os.path.dirname(                                        # Project
                        os.path.dirname(                                    # Year
                            os.path.dirname(os.path.abspath(__file__)))))   # Day

    from helpers import Timer

    with open("input.txt", "r") as file:
        sequence, nodes = file.read().strip().split('\n\n')

    # --- Part 1 --- #
    with Timer():
        print("Nb of steps required to reach the exit:",
              count_steps_to_exit(sequence.strip(), nodes.split('\n')))  # 21797

    # --- Part 2 --- #
    with Timer():
        print("Nb of simultaneous steps required to reach the exit:",
              count_simultaneous_steps_to_exit(sequence.strip(), nodes.split('\n')))  # 23977527174353


if __name__ == "__main__":
    main()
