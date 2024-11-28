# Advent of Code : Day 20 - Grove Positioning System
# https://adventofcode.com/2022/day/20

import os

from helpers import Timer


@Timer.timeit
def decrypt(
    array: list[int],
    decryption_key: int,
    nb_rounds: int,
    indexes: list[int] = [1000, 2000, 3000],
) -> int:
    array = [decryption_key * val for val in array]
    n = len(array)
    indices = list(range(n))

    for i in indices * nb_rounds:
        indices.pop(j := indices.index(i))
        indices.insert((j + array[i]) % (n - 1), i)

    zero_pos = indices.index(array.index(0))
    return sum(array[indices[(zero_pos + index) % n]] for index in indexes)


@Timer.timeit
def parse(filename: os.PathLike) -> list[int]:
    with open(filename, "r") as file:
        array = list(map(int, file.read().strip().split("\n")))
    return array


@Timer.timeit
def solve(filename: os.PathLike) -> tuple[int, int]:
    array = parse(filename)
    part1 = decrypt(array, 1, 1)
    part2 = decrypt(array, 811589153, 10)

    return part1, part2
