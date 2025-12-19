# Advent of Code : Day 04 - Printing Department
# https://adventofcode.com/2025/day/4

from collections.abc import Iterable

from helpers import Timer, load_input_data

MAX_PAPER_ROLLS = 4


def pad(grid: Iterable[Iterable[int]]) -> list[list[int]]:
    m, n = len(grid), len(grid[0])
    padded = [[0 for _ in range(n + 2)] for _ in range(m + 2)]
    for i in range(m):
        for j in range(n):
            padded[i + 1][j + 1] = grid[i][j]
    return padded


def get_accessible_paper_rolls(grid: Iterable[Iterable[int]]) -> list[tuple[int, int]]:
    def convolve(x: int, y: int) -> int:
        return sum(grid[x + dx][y + dy] for dx in (-1, 0, 1) for dy in (-1, 0, 1))

    accessible = list()
    m, n = len(grid), len(grid[0])
    for i in range(1, m - 1):
        for j in range(1, n - 1):
            if grid[i][j] and convolve(i, j) < MAX_PAPER_ROLLS + 1:
                accessible.append((i, j))

    return accessible


def get_removable_paper_rolls(
    padded_grid: Iterable[Iterable[int]], max_iter: int = -1
) -> int:
    removed = 0
    nb_iter = 0
    # Basically a mark ans sweep algorithm
    while nb_iter != max_iter:
        nb_iter += 1
        accessible = get_accessible_paper_rolls(padded_grid)

        if not accessible:
            # Cannot remove any more paper rolls
            break

        # Remove accessible paper rolls
        for i, j in accessible:
            padded_grid[i][j] = 0
        removed += len(accessible)

    return removed


@Timer.timeit
def parse(data: str) -> list[list[int]]:
    m = {".": 0, "@": 1}
    return [list(map(lambda c: m[c], row)) for row in data.split("\n")]


@Timer.timeit
def solve(data: str) -> tuple[int, int]:
    padded_grid = pad(parse(data))
    part1 = get_removable_paper_rolls(padded_grid, 1)
    part2 = part1 + get_removable_paper_rolls(padded_grid)

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2025, 4)))
