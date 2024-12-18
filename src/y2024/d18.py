# Advent of Code : Day 18 - RAM Run
# https://adventofcode.com/2024/day/18

from collections import deque

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
def find_last_fallen_byte(falling_bytes: list[complex], N: int, T: int) -> str:
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
    part2 = find_last_fallen_byte(falling_bytes, 70, 1024)

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2024, 18)))
