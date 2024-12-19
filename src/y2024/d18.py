# Advent of Code : Day 18 - RAM Run
# https://adventofcode.com/2024/day/18

from collections import deque
from dataclasses import dataclass
from itertools import product
from typing import Self

from helpers import Timer, load_input_data


def simulate(fallen_bytes: set[complex], N: int) -> int:
    source = complex(0, 0)
    target = complex(N, N)

    queue: deque[tuple[int, complex]] = deque([(0, source)])
    visited = set([source])

    while queue:
        t, curr = queue.popleft()

        if curr == target:
            return t

        for d in (-1j, 1j, -1, 1):
            adj = curr + d

            if adj in visited:
                continue

            if adj in fallen_bytes:
                continue

            if not all(0 <= k <= N for k in (adj.real, adj.imag)):
                continue

            queue.append((t + 1, adj))
            visited.add(adj)

    return 0


@Timer.timeit
def find_shortest_path(falling_bytes: list[complex], N: int, T: int) -> int:
    return simulate(set(falling_bytes[:T]), N)


@Timer.timeit
def find_closing_byte(falling_bytes: list[complex], N: int, T: int) -> str:
    lo, hi = T, len(falling_bytes)

    while lo <= hi:
        mid = (lo + hi) // 2

        if mid == lo:
            break

        if simulate(set(falling_bytes[:mid]), N):
            lo = mid
        else:
            hi = mid

    z = falling_bytes[mid]
    return f"{int(z.real)},{int(z.imag)}"


@Timer.timeit
def find_closing_byte2(falling_bytes: list[complex], N: int) -> str:
    @dataclass
    class UnionFind:
        color: int
        prev: Self | None = None

        def find(self) -> Self:
            if self.prev is None:
                return self
            self.prev = self.prev.find()
            return self.prev

        def merge(self, other: Self) -> None:
            ps = self.find()
            po = other.find()
            if ps is not po:
                ps.prev = po
                po.color |= ps.color

    def get_group(z: complex) -> int:
        x, y = map(int, (z.real, z.imag))
        if x == N or y == 0:
            return 0b10  # Belongs to Top-Right group
        elif x == 0 or y == N:
            return 0b01  # Belongs to Bottom-Left group
        else:
            return 0b00  # Does not belong to any group

    fallen: dict[complex, UnionFind] = {}
    adjacency = set(complex(x, y) for x, y in product((-1, 0, 1), repeat=2)) - {0j}
    for b in falling_bytes:
        b_uf = UnionFind(get_group(b))
        fallen[b] = b_uf

        for d in adjacency:
            if (adj := b + d) in fallen:
                b_uf.merge(fallen[adj])

        # Belongs to both Top-Right and Bottom-Left groups
        # i.e., there is a connection between both groups and so,
        # there is no possible path from (0, 0) to (N, N)
        if b_uf.find().color == 0b11:
            return f"{int(b.real)},{int(b.imag)}"

    return ""


@Timer.timeit
def parse(data: str) -> list[complex]:
    falling_bytes = []
    for coord in data.splitlines():
        x, y = map(int, coord.split(","))
        falling_bytes.append(complex(x, y))
    return falling_bytes


@Timer.timeit
def solve(data: str) -> tuple[int, str]:
    falling_bytes = parse(data)
    part1 = find_shortest_path(falling_bytes, 70, 1024)
    part2 = find_closing_byte(falling_bytes, 70, 1024)
    # part2 = find_closing_byte2(falling_bytes, 70)

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2024, 18)))
