# Advent of Code : Day 16 - Proboscidea Volcanium
# https://adventofcode.com/2022/day/16


from dataclasses import dataclass
from typing import Dict, List
from collections import defaultdict

def adj_matrix_factory():
    return 9999


def floydWarshall(adj_matrix: Dict) -> Dict:
    for k in adj_matrix.keys():
        for i in adj_matrix.keys():
            for j in adj_matrix.keys():
                if i == j:
                    continue

                adj_matrix[i][j] = min(adj_matrix[i][j], adj_matrix[i][k] + adj_matrix[k][j])
                adj_matrix[j][i] = adj_matrix[i][j]

    return adj_matrix


@dataclass
class State:
    curr: str
    t: int = 1
    pressure_released: int = 0
    opened: list = []
    path: list = []


def main():
    t_final = 30
    start_label = 'AA'
    adj_matrix = dict()

    max_pressure_released = 0
    max_pressure_path = []

    with open('input2.txt', 'r') as file:
        for line in file:
            line = line.strip().split()

            label = line[1]
            flow = int(line[4].rstrip(';').split('=')[-1])
            adj = [neighbour.rstrip(',') for neighbour in line[9:]]

            # print(f"{label=} {flow=} {adj=}")

            adj_matrix[label] = defaultdict(adj_matrix_factory)
            adj_matrix[label][label] = flow
            for neighbour in adj:
                adj_matrix[label][neighbour] = 1


    adj_matrix = floydWarshall(adj_matrix)

    # Answer part 1
    print(max_pressure_path)
    print(max_pressure_released)

    # Answer part 2

if __name__ == "__main__":
    main()