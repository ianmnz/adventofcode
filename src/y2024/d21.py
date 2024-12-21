# Advent of Code : Day 21 - Keypad Conundrum
# https://adventofcode.com/2024/day/21

import itertools
from collections import deque
from functools import cache

from helpers import Timer, load_input_data

DIRS = {
    -1 + 0j: "^",
    0 + 1j: ">",
    1 + 0j: "v",
    0 - 1j: "<",
}

NUM_PAD = {
    0 + 0j: "7",
    0 + 1j: "8",
    0 + 2j: "9",
    1 + 0j: "4",
    1 + 1j: "5",
    1 + 2j: "6",
    2 + 0j: "1",
    2 + 1j: "2",
    2 + 2j: "3",
    3 + 1j: "0",
    3 + 2j: "A",
}
NUM_PAD_INV = {v: k for k, v in NUM_PAD.items()}
NUM_PAD_TRANSITION = {}

DIR_PAD = {
    0 + 1j: "^",
    0 + 2j: "A",
    1 + 0j: "<",
    1 + 1j: "v",
    1 + 2j: ">",
}
DIR_PAD_INV = {v: k for k, v in DIR_PAD.items()}
DIR_PAD_TRANSITION = {}


def bfs(pad: dict[complex, str], source: complex, target: complex) -> list[str]:
    min_seq_len = float("inf")
    transitions = []

    queue: deque[tuple[complex, str]] = deque([(source, "")])
    while queue:
        z, seq = queue.popleft()

        if len(seq) > min_seq_len:
            continue

        if z == target:
            min_seq_len = len(seq)
            transitions.append(seq)
            continue

        for d, b in DIRS.items():
            zd = z + d
            if zd in pad:
                queue.append((zd, seq + b))

    return transitions


@Timer.timeit
def pre_compute(codes: list[str]) -> None:
    global NUM_PAD_TRANSITION, DIR_PAD_TRANSITION

    num_comb = {(s, t) for code in codes for s, t in itertools.pairwise("A" + code)}
    for s, t in num_comb:
        transitions = bfs(NUM_PAD, NUM_PAD_INV[s], NUM_PAD_INV[t])
        NUM_PAD_TRANSITION[(s, t)] = [tr + "A" for tr in transitions]

    for s, t in itertools.product(DIR_PAD.values(), repeat=2):
        transitions = bfs(DIR_PAD, DIR_PAD_INV[s], DIR_PAD_INV[t])
        DIR_PAD_TRANSITION[(s, t)] = [tr + "A" for tr in transitions]

    return


@cache
def expand(seq: str, depth: int) -> int:
    if depth == 0:
        return len(seq)

    res = 0
    for s, t in itertools.pairwise("A" + seq):
        res += min(
            expand(expansion, depth - 1) for expansion in DIR_PAD_TRANSITION[(s, t)]
        )

    return res


def get_complexity(code: str, max_depth: int) -> int:
    subseqs = [NUM_PAD_TRANSITION[(s, t)] for s, t in itertools.pairwise("A" + code)]
    seqs = ["".join(prod) for prod in itertools.product(*subseqs)]
    return int(code[:-1]) * min(expand(seq, max_depth) for seq in seqs)


@Timer.timeit
def get_total_complexity(codes: list[str], max_depth: int) -> int:
    return sum(get_complexity(code, max_depth) for code in codes)


@Timer.timeit
def parse(data: str) -> list[str]:
    return data.splitlines()


@Timer.timeit
def solve(data: str) -> tuple[int, int]:
    codes = parse(data)
    pre_compute(codes)
    part1 = get_total_complexity(codes, 2)
    part2 = get_total_complexity(codes, 25)

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2024, 21)))
