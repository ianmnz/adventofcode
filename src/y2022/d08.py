# Advent of Code : Day 08 - Treetop Tree House
# https://adventofcode.com/2022/day/8

import os
from typing import List, Tuple

from helpers import Timer

Grid = List[List[int]]


@Timer.timeit
def transpose(grid: Grid) -> Grid:
    return [[grid[j][i] for j in range(len(grid))] for i in range(len(grid[0]))]


def get_line_of_sight(j: int, row: List[int]) -> Tuple[int, int]:
    n = len(row)

    l_score = j
    r_score = j
    for k in range(1, j):
        if row[j - k] >= row[j]:
            l_score = k
            break

    for k in range(1, j):
        if row[n - j - 1 + k] >= row[n - j - 1]:
            r_score = k
            break

    return l_score, r_score


@Timer.timeit
def traverse_grid_per_row(grid: Grid, exposure: Grid, score: Grid) -> None:
    n = len(grid[0])

    for i, row in enumerate(grid):
        # Edge tree - first column
        leftmost_visible_height = row[0]
        exposure[i][0] = 1
        score[i][0] = 0

        # Edge tree - last column
        rightmost_visible_height = row[n - 1]
        exposure[i][n - 1] = 1
        score[i][n - 1] = 0

        for j, col in enumerate(row[1 : n - 1], 1):
            n_j_1 = n - j - 1

            l_height = col
            r_height = row[n_j_1]

            # Tree is visible coming from the left
            if l_height > leftmost_visible_height:
                leftmost_visible_height = l_height
                exposure[i][j] = 1

            # Tree is visible coming from the right
            if r_height > rightmost_visible_height:
                rightmost_visible_height = r_height
                exposure[i][n_j_1] = 1

            l_score, r_score = get_line_of_sight(j, row)
            score[i][j] *= l_score
            score[i][n_j_1] *= r_score


@Timer.timeit
def compute_exposure_and_score(grid: Grid) -> Tuple[Grid, Grid]:
    m, n = len(grid), len(grid[0])

    exposure = [[0 for j in range(n)] for i in range(m)]
    score = [[1 for j in range(n)] for i in range(m)]

    traverse_grid_per_row(grid, exposure, score)

    grid = transpose(grid)
    exposure = transpose(exposure)
    score = transpose(score)
    traverse_grid_per_row(grid, exposure, score)

    return exposure, score


@Timer.timeit
def count_nb_visible_trees(exposure: Grid) -> int:
    return sum(map(sum, exposure))


@Timer.timeit
def get_highest_scenic_score(score: Grid) -> int:
    return max(map(max, score))


@Timer.timeit
def parse(filename: os.PathLike) -> Grid:
    with open(filename, "r") as file:
        grid = [
            [int(char) for char in line] for line in file.read().strip().split("\n")
        ]
    return grid


@Timer.timeit
def solve(filename: os.PathLike) -> Tuple[int, int]:
    grid = parse(filename)
    exposure, score = compute_exposure_and_score(grid)
    part1 = count_nb_visible_trees(exposure)
    part2 = get_highest_scenic_score(score)

    return part1, part2
