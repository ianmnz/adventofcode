# Advent of Code : Day 20 - Grove Positioning System
# https://adventofcode.com/2022/day/20

from typing import List, Tuple

from helpers import Timer


@Timer.timeit
def decrypt(
    array: List[int],
    decryption_key: int,
    nb_rounds: int,
    indexes: List[int] = [1000, 2000, 3000],
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
def parse(filename: str) -> List[int]:
    with open(filename, "r") as file:
        array = list(map(int, file.read().strip().split("\n")))
    return array


@Timer.timeit
def solve(filename: str) -> Tuple[int, int]:
    array = parse(filename)
    part1 = decrypt(array, 1, 1)
    part2 = decrypt(array, 811589153, 10)

    return part1, part2


def main() -> None:
    import os

    res = solve(os.path.dirname(os.path.abspath(__file__)) + "/input.txt")

    assert res[0] == 6712, f"Part1 = {res[0]}"
    assert res[1] == 1595584274798, f"Part2 = {res[1]}"


if __name__ == "__main__":
    main()
