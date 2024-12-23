# Advent of Code : Day 22 - Monkey Market
# https://adventofcode.com/2024/day/22

import itertools
from collections import defaultdict

from helpers import Timer, load_input_data

MASK = (1 << 24) - 1  # == 16_777_216 - 1


def generate(secret: int, nb_iter: int) -> list[int]:
    seq = [0] * (nb_iter + 1)
    for i in range(nb_iter):
        seq[i] = secret

        secret = (secret ^ (secret << 6)) & MASK
        secret = (secret ^ (secret >> 5)) & MASK
        secret = (secret ^ (secret << 11)) & MASK

    seq[nb_iter] = secret
    return seq


@Timer.timeit
def speculate(secrets: list[int], nb_iter: int):
    # Based on:
    # https://www.reddit.com/r/adventofcode/comments/1hjroap/comment/m38uybz/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
    # https://www.reddit.com/r/adventofcode/comments/1hjroap/comment/m392gz6/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
    total = 0
    bananas = defaultdict(int)

    for secret in secrets:
        seq = generate(secret, nb_iter)
        total += seq[-1]

        prices = list(map(lambda x: x % 10, seq))
        diffs = [curr - prev for prev, curr in itertools.pairwise(prices)]

        patterns = set()
        for i in range(len(seq) - 4):
            # A numerical key is faster than a tuple
            # Since they are in the range -9-9, this can be seen as a base 20 number
            # The operation bellow is equivalent to joining a string in
            # such base and then and casting it to int
            pattern = (
                diffs[i] * 8000 + diffs[i + 1] * 400 + diffs[i + 2] * 20 + diffs[i + 3]
            )

            if pattern not in patterns:
                bananas[pattern] += prices[i + 4]
                patterns.add(pattern)

    return total, max(bananas.values())


@Timer.timeit
def parse(data: str) -> list[int]:
    return list(map(int, data.splitlines()))


@Timer.timeit
def solve(data: str) -> tuple[int, int]:
    secrets = parse(data)
    part1, part2 = speculate(secrets, 2000)

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2024, 22)))
