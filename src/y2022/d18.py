# Advent of Code : Day 18 - Boiling Boulders
# https://adventofcode.com/2022/day/18

import os

from helpers import Timer


@Timer.timeit
def get_surface_area(droplets: list[tuple[int, ...]]) -> int:
    nb_faces = 6 * len(droplets)

    for x, y, z in (cubes := set(droplets)):
        if (x, y, z + 1) in cubes:
            nb_faces -= 2

        if (x, y + 1, z) in cubes:
            nb_faces -= 2

        if (x + 1, y, z) in cubes:
            nb_faces -= 2

    return nb_faces


@Timer.timeit
def get_external_surface_area(droplets: list[tuple[int, ...]]) -> int:
    cubes = set(droplets)

    x_lower, x_upper = float("inf"), float("-inf")
    y_lower, y_upper = float("inf"), float("-inf")
    z_lower, z_upper = float("inf"), float("-inf")

    for x, y, z in cubes:
        x_lower, x_upper = min(x_lower, x), max(x, x_upper)
        y_lower, y_upper = min(y_lower, y), max(y, y_upper)
        z_lower, z_upper = min(z_lower, z), max(z, z_upper)

    x_lower -= 1
    x_upper += 1
    y_lower -= 1
    y_upper += 1
    z_lower -= 1
    z_upper += 1

    nb_faces = 0

    # Flood-fill algorithm
    queue = [(x_lower, y_lower, z_lower)]
    visited = {queue[0]}
    is_valid = (
        lambda x, y, z: (x_lower <= x <= x_upper)
        and (y_lower <= y <= y_upper)
        and (z_lower <= z <= z_upper)
    )

    while queue:
        x, y, z = queue.pop()

        for dx in (-1, 1):
            next = (x + dx, y, z)
            if next in cubes:
                nb_faces += 1

            elif (next not in visited) and is_valid(*next):
                visited.add(next)
                queue.append(next)

        for dy in (-1, 1):
            next = (x, y + dy, z)
            if next in cubes:
                nb_faces += 1

            elif (next not in visited) and is_valid(*next):
                visited.add(next)
                queue.append(next)

        for dz in (-1, 1):
            next = (x, y, z + dz)
            if next in cubes:
                nb_faces += 1

            elif (next not in visited) and is_valid(*next):
                visited.add(next)
                queue.append(next)

    return nb_faces


@Timer.timeit
def parse(filename: os.PathLike) -> list[tuple[int, ...]]:
    with open(filename, "r") as file:
        droplets = [
            tuple(map(int, droplet.split(",")))
            for droplet in file.read().strip().split("\n")
        ]
    return droplets


@Timer.timeit
def solve(filename: os.PathLike) -> tuple[int, int]:
    droplets = parse(filename)
    part1 = get_surface_area(droplets)
    part2 = get_external_surface_area(droplets)

    return part1, part2
