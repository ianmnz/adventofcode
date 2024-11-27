# Advent of Code : Day 24 - Blizzard Basin
# https://adventofcode.com/2022/day/24

import heapq
import os
from typing import List, Set, Tuple

from helpers import Timer

Grid = List[List[int]]
State = Tuple[int, int, int]


bitmask = {
    ".": 0,
    ">": 1,
    "<": 2,
    "^": 4,
    "v": 8,
    "#": 16,
}


def generate_next_grid(curr_grid: Grid) -> Grid:
    m, n = len(curr_grid), len(curr_grid[0])
    mod_m, mod_n = (m - 2), (n - 2)

    next_grid = [[0 for j in range(n)] for i in range(m)]

    for i, row in enumerate(curr_grid):
        for j, col in enumerate(row):
            if col == bitmask["#"]:
                next_grid[i][j] = col

            else:
                if col & bitmask[">"]:
                    next_grid[i][j % mod_n + 1] |= bitmask[">"]

                if col & bitmask["<"]:
                    next_grid[i][(j - 2) % mod_n + 1] |= bitmask["<"]

                if col & bitmask["v"]:
                    next_grid[i % mod_m + 1][j] |= bitmask["v"]

                if col & bitmask["^"]:
                    next_grid[(i - 2) % mod_m + 1][j] |= bitmask["^"]

    return next_grid


def bfs(
    t0: int, source: Tuple[int, int], target: Tuple[int, int], history: List[Grid]
) -> int:
    m, n = len(history[0]), len(history[0][0])

    # To avoid cycling, there are no more than lcm(m-2, n-2) possible
    # grids. However, since in the input n-2 is prime, lcm = (m - 2) * (n - 2)
    # Normally, we won't need as much grids
    lcm = (m - 2) * (n - 2)

    queue: List[State] = [(t0, *source)]
    visited: Set[State] = set()

    while queue:
        t, x, y = heapq.heappop(queue)

        if (x, y) == target:
            return t

        tdt = t + 1
        history_index = tdt % lcm

        if history_index == len(history):
            history.append(generate_next_grid(history[-1]))
        next_grid = history[history_index]

        for dx, dy in [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]:
            xdx = x + dx
            ydy = y + dy

            if 0 <= xdx < m and (tdt, xdx, ydy) not in visited:
                if next_grid[xdx][ydy] == 0:
                    heapq.heappush(queue, (tdt, xdx, ydy))
                    visited.add((tdt, xdx, ydy))

    return -1


@Timer.timeit
def get_time_to_cross_valley(grid: Grid, with_return: bool = False) -> int:
    m = len(grid)

    source = 0, grid[0].index(0)
    target = m - 1, grid[m - 1].index(0)
    history = [grid]

    if not with_return:
        return bfs(0, source, target, history)

    else:
        t_reach_target = bfs(0, source, target, history)
        t_back_source = bfs(t_reach_target, target, source, history)
        t_back_target = bfs(t_back_source, source, target, history)

        return t_back_target


@Timer.timeit
def parse(filename: os.PathLike) -> Grid:
    with open(filename, "r") as file:
        grid = [
            [bitmask[char] for char in line] for line in file.read().strip().split("\n")
        ]
    return grid


@Timer.timeit
def solve(filename: os.PathLike) -> Tuple[int, int]:
    grid = parse(filename)
    part1 = get_time_to_cross_valley(grid)
    part2 = get_time_to_cross_valley(grid, True)

    return part1, part2


def main() -> None:
    from pathlib import Path

    res = solve(Path(__file__).parent / "input.txt")

    assert res[0] == 322, f"Part1 = {res[0]}"
    assert res[1] == 974, f"Part2 = {res[1]}"


if __name__ == "__main__":
    main()
