# Advent of Code : Day 21 - Step Counter
# https://adventofcode.com/2023/day/21

import collections

from helpers import Timer, load_input_data


@Timer.timeit
def nb_reachable_gardens(
    grid: list[list[str]], nb_steps: int = 64, with_repetition: bool = False
) -> int:
    n = len(grid)
    m = len(grid[0])
    start = complex(n // 2, m // 2)

    def is_valid(z: complex) -> bool:
        x, y = int(z.real), int(z.imag)
        if with_repetition:
            return grid[x % n][y % m] != "#"
        else:
            return (0 <= x < n) and (0 <= y < m) and grid[x][y] != "#"

    queue = collections.deque()
    queue.append((0, start))
    reached = 0
    visited = set()

    while queue:
        steps, curr = queue.popleft()

        if curr in visited:
            continue

        visited.add(curr)
        if nb_steps % 2 == steps % 2:
            reached += 1

        if steps == nb_steps:
            continue

        up = curr + (-1 + 0j)
        down = curr + (1 + 0j)
        left = curr + (0 + -1j)
        right = curr + (0 + 1j)

        if is_valid(up):
            queue.append((steps + 1, up))

        if is_valid(down):
            queue.append((steps + 1, down))

        if is_valid(left):
            queue.append((steps + 1, left))

        if is_valid(right):
            queue.append((steps + 1, right))

    return reached


@Timer.timeit
def quadratic_interpolation(grid: list[list[str]], nb_steps: int = 26501365) -> int:
    n = len(grid)

    y0 = nb_reachable_gardens(grid, n // 2 + 0 * n, True)
    y1 = nb_reachable_gardens(grid, n // 2 + 1 * n, True)
    y2 = nb_reachable_gardens(grid, n // 2 + 2 * n, True)

    a = (y2 - 2 * y1 + y0) // 2
    b = (y1 - y0) - a
    c = y0
    x = nb_steps // n
    return (a * x**2) + (b * x) + c


@Timer.timeit
def parse(data: str) -> list[list[str]]:
    return [[char for char in line] for line in data.split("\n")]


@Timer.timeit
def solve(data: str) -> tuple[int, int]:
    grid = parse(data)
    part1 = nb_reachable_gardens(grid, 64)
    part2 = quadratic_interpolation(grid, 26501365)

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2023, 21)))
