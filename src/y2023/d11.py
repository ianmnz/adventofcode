# Advent of Code : Day 11 - Cosmic Expansion
# https://adventofcode.com/2023/day/11

import os

from helpers import Timer


@Timer.timeit
def compute_distances_matrix(image: list[str], expansion: int) -> list[list[int]]:
    empty_rows = set(range(len(image)))
    empty_cols = set(range(len(image[0])))

    galaxies = []

    for i, row in enumerate(image):
        for j, col in enumerate(row):
            if col == "#":
                empty_rows.discard(i)
                empty_cols.discard(j)
                galaxies.append((i, j))

    n = len(galaxies)
    distances = [[0 for _ in range(n)] for _ in range(n)]

    for a in range(n):
        galaxy_a = galaxies[a]
        for b in range(a + 1, n):
            galaxy_b = galaxies[b]

            low_i, upp_i = sorted((galaxy_a[0], galaxy_b[0]))
            dist_i = (upp_i - low_i) + sum(
                [expansion - 1 if low_i < row < upp_i else 0 for row in empty_rows]
            )

            low_j, upp_j = sorted((galaxy_a[1], galaxy_b[1]))
            dist_j = (upp_j - low_j) + sum(
                [expansion - 1 if low_j < col < upp_j else 0 for col in empty_cols]
            )

            distances[a][b] = distances[b][a] = int(
                dist_i + dist_j
            )  # manhattan distance

    return distances


@Timer.timeit
def calculate_sum_of_distances(image: list[str], expansion: int) -> int:
    distances = compute_distances_matrix(image, expansion)
    return sum(map(sum, distances)) // 2


@Timer.timeit
def parse(filename: os.PathLike) -> list[str]:
    with open(filename, "r") as file:
        image = file.read().split("\n")
    return image


@Timer.timeit
def solve(filename: os.PathLike) -> tuple[int, int]:
    image = parse(filename)
    part1 = calculate_sum_of_distances(image, 2)
    part2 = calculate_sum_of_distances(image, 1_000_000)

    return part1, part2
