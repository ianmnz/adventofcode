# Advent of Code : Day 08 - Playground
# https://adventofcode.com/2025/day/8

import heapq
import operator
from collections.abc import Generator, Iterable
from functools import reduce
from operator import itemgetter
from typing import NamedTuple

from helpers import Timer, load_input_data


class Pos3D(NamedTuple):
    x: int
    y: int
    z: int


def dist_sqr(u: Pos3D, v: Pos3D) -> int:
    def sqr(x: int) -> int:
        return x * x

    return sqr(u.x - v.x) + sqr(u.y - v.y) + sqr(u.z - v.z)


class Circuits:
    roots: list[int]
    sizes: list[int]

    def __init__(self, n: int) -> None:
        self.roots = list(range(n))
        self.sizes = [1] * n

    def size_of(self, i: int) -> int:
        return self.sizes[self.roots[i]]

    def find(self, i: int) -> int:
        root = self.roots[i]
        if self.roots[root] != root:
            self.roots[i] = self.find(root)
            return self.roots[i]
        return root

    def unite(self, i: int, j: int) -> None:
        root_i = self.find(i)
        root_j = self.find(j)

        if root_i == root_j:
            return

        size_i = self.sizes[root_i]
        size_j = self.sizes[root_j]

        if size_i < size_j:
            self.roots[root_i] = root_j
            self.sizes[root_j] += size_i
            self.sizes[root_i] = 0
        else:
            self.roots[root_j] = root_i
            self.sizes[root_i] += size_j
            self.sizes[root_j] = 0


def connect_junction_boxes(
    positions: Iterable[Pos3D], nb_circuits: int, nb_distances: int
) -> Generator[int, None, int]:
    nb_pos = len(positions)
    distances = sorted(
        [
            (i, j, dist_sqr(positions[i], positions[j]))
            for i in range(nb_pos)
            for j in range(i + 1, nb_pos)
        ],
        key=itemgetter(2),
    )

    circuits = Circuits(len(distances))

    for i, j, _ in distances[:nb_distances]:
        circuits.unite(i, j)

    yield reduce(operator.mul, heapq.nlargest(nb_circuits, circuits.sizes))

    for i, j, _ in distances[nb_distances:]:
        circuits.unite(i, j)

        if circuits.size_of(i) == nb_pos or circuits.size_of(j) == nb_pos:
            yield positions[i].x * positions[j].x
            break

    return -1


@Timer.timeit
def parse(data: str) -> Iterable[Pos3D]:
    return [Pos3D(*map(int, row.split(","))) for row in data.split("\n")]


@Timer.timeit
def solve(data: str) -> tuple[int, int]:
    positions = parse(data)
    tmp_g = connect_junction_boxes(positions, 3, 1000)
    part1 = next(tmp_g)
    part2 = next(tmp_g)

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2025, 8)))
