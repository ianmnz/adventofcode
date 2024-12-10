# Advent of Code : Day 10 - Hoof It
# https://adventofcode.com/2024/day/10

from helpers import Timer, load_input_data


@Timer.timeit
def add_padding(grid: list[list[int]], pad: int, val: int = -1) -> list[list[int]]:
    n = len(grid[0])

    pad_row = [val] * (n + 2 * pad)
    pad_col = [val] * pad
    return [pad_row] * pad + [pad_col + row + pad_col for row in grid] + [pad_row] * pad


def get_trailhead_measures(
    start: tuple[int, int], grid: list[list[int]]
) -> tuple[int, int]:
    score = set()
    rating = 0

    stack = [start]

    while stack:
        i, j = stack.pop()
        curr = grid[i][j]

        if curr == 9:
            score.add((i, j))
            rating += 1
            continue

        next = curr + 1

        # UP
        if grid[i - 1][j] == next:
            stack.append((i - 1, j))

        # DOWN
        if grid[i + 1][j] == next:
            stack.append((i + 1, j))

        # LEFT
        if grid[i][j - 1] == next:
            stack.append((i, j - 1))

        # RIGHT
        if grid[i][j + 1] == next:
            stack.append((i, j + 1))

    return len(score), rating


@Timer.timeit
def get_topographic_map_score(topographic_map: list[list[int]]) -> tuple[int, int]:
    m = len(topographic_map)
    n = len(topographic_map[0])
    pad = 1

    grid = add_padding(topographic_map, pad)

    score = 0
    rating = 0
    for i in range(pad, m + pad):
        for j in range(pad, n + pad):
            if grid[i][j]:
                continue

            s, r = get_trailhead_measures((i, j), grid)

            score += s
            rating += r

    return score, rating


@Timer.timeit
def parse(data: str) -> list[list[int]]:
    return [[int(col) for col in row] for row in data.splitlines()]


@Timer.timeit
def solve(data: str) -> tuple[int, int]:
    topographic_map = parse(data)
    part1, part2 = get_topographic_map_score(topographic_map)

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2024, 10)))
