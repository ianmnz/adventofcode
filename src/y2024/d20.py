# Advent of Code : Day 20 - Race Condition
# https://adventofcode.com/2024/day/20

from typing import NamedTuple

from helpers import Timer, load_input_data


class Vec2D(NamedTuple):
    x: int
    y: int


M, N = -1, -1


@Timer.timeit
def mark_racetrack_path(
    racetrack: list[list[str]],
) -> tuple[list[Vec2D], list[list[int]]]:
    start = next(
        Vec2D(i, j)
        for i, row in enumerate(racetrack)
        for j, col in enumerate(row)
        if col == "S"
    )
    end = next(
        Vec2D(i, j)
        for i, row in enumerate(racetrack)
        for j, col in enumerate(row)
        if col == "E"
    )

    global M, N
    M = len(racetrack)
    N = len(racetrack[0])

    grid = [[-1 for _ in range(N)] for _ in range(M)]
    grid[start.x][start.y] = 0

    path = [start]

    t, curr = 0, start
    while curr != end:
        for dx, dy in (-1, 0), (1, 0), (0, 1), (0, -1):
            new = Vec2D(curr.x + dx, curr.y + dy)

            if grid[new.x][new.y] == -1 and racetrack[new.x][new.y] in ".E":
                grid[new.x][new.y] = t + 1
                path.append(new)

                curr = new
                t += 1
                break

    return path, grid


def find_shortcuts(
    center: Vec2D, max_radius: int, grid: list[list[int]]
) -> set[tuple[int, Vec2D]]:
    shortcuts = set()

    cx, cy = center
    for r in range(2, max_radius + 1):
        for dx in range(-r, r + 1):
            dy = r - abs(dx)  # Manhattan distance

            cdx = cx + dx
            cdy_p = cy + dy  # dy+
            cdy_n = cy - dy  # dy-

            if not 0 < cdx < M - 1:
                continue

            if 0 < cdy_p < N - 1 and grid[cdx][cdy_p] >= 0:
                shortcuts.add((r, Vec2D(cdx, cdy_p)))

            if 0 < cdy_n < N - 1 and grid[cdx][cdy_n] >= 0:
                shortcuts.add((r, Vec2D(cdx, cdy_n)))

    return shortcuts


@Timer.timeit
def count_shortcuts(
    path: list[Vec2D], grid: list[list[int]], max_length: int, saved_time: int
) -> int:
    ans = 0
    for t, curr in enumerate(path):
        for sc_len, sc_pos in find_shortcuts(curr, max_length, grid):
            if (grid[sc_pos.x][sc_pos.y] - t - sc_len) >= saved_time:
                # Offset by sc_len for the nb of time steps spent arriving here
                ans += 1

    return ans


@Timer.timeit
def parse(data: str) -> list[list[str]]:
    return [[col for col in row] for row in data.splitlines()]


@Timer.timeit
def solve(data: str) -> tuple[int, int]:
    racetrack = parse(data)
    path, grid = mark_racetrack_path(racetrack)
    part1 = count_shortcuts(path, grid, 2, 100)
    part2 = count_shortcuts(path, grid, 20, 100)

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2024, 20)))
