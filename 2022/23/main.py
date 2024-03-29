# Advent of Code : Day 23 - Unstable Diffusion
# https://adventofcode.com/2022/day/23

from collections import defaultdict
from dataclasses import dataclass
from itertools import product
from typing import Dict, List, Set, Tuple

from helpers import Timer

N = 0 - 1j
S = 0 + 1j
E = 1 + 0j
W = -1 + 0j

kernel = {
    0j: 0,  # Center
    N: 1,  # North
    S: 2,  # South
    W: 4,  # West
    E: 8,  # East
    N + W: 5,  # NW
    S + W: 6,  # SW
    N + E: 9,  # NE
    S + E: 10,  # SE
}

cycle = [N, S, W, E]
cycle_len = len(cycle)
cycle_start = 0


@dataclass
class Elf:
    # Elf cellular automata
    pos: complex

    def check_surrounding(self, other_pos: Set[complex]) -> int:
        res = 0
        for dx, dy in product((-1, 0, 1), repeat=2):
            dz = complex(dx, dy)
            if self.pos + dz in other_pos:
                res |= kernel[dz]
        return res


def round(elves: List[Elf]) -> bool:
    curr_pos = {elf.pos for elf in elves}
    propositions: Dict[complex, List[Elf]] = defaultdict(list)

    for elf in elves:
        # First half:
        # Check surroundings for another elf
        # If any other elf in the surroundings, proposes to move
        # Then checks where these other elves are and moves away
        # following the cycle, starting from the cycle_start
        if surrounding := elf.check_surrounding(curr_pos):
            for i in range(4):
                idx = (cycle_start + i) % cycle_len
                if not ((1 << idx) & surrounding):
                    propositions[elf.pos + cycle[idx]].append(elf)
                    break

    # Second half:
    # We check the propositions and try to move the elves
    # if no elf moved, we return false
    did_any_elf_move = False
    for pos, candidates in propositions.items():
        if len(candidates) == 1:
            candidates[0].pos = pos
            did_any_elf_move = True

    return did_any_elf_move


@Timer.timeit
def spread(elves: List[Elf], nb_rounds: int) -> int:
    # A kind of game of life
    global cycle_start

    for n in range(1, nb_rounds + 1):
        if not round(elves):
            break
        cycle_start = (cycle_start + 1) % cycle_len

    return n


@Timer.timeit
def get_covered_ground(elves: List[Elf]) -> int:
    x_min = y_min = float("inf")
    x_max = y_max = float("-inf")

    for elf in elves:
        x_min = min(x_min, elf.pos.real)
        y_min = min(y_min, elf.pos.imag)
        x_max = max(x_max, elf.pos.real)
        y_max = max(y_max, elf.pos.imag)

    return int((x_max - x_min + 1) * (y_max - y_min + 1)) - len(elves)


@Timer.timeit
def parse(filename: str) -> List[Elf]:
    with open(filename, "r") as file:
        lines = file.read().strip().split("\n")

    return [
        Elf(complex(x, y))
        for y, line in enumerate(lines)
        for x, col in enumerate(line)
        if col == "#"
    ]


@Timer.timeit
def solve(filename: str) -> Tuple[int, int]:
    elves = parse(filename)
    spread(elves, 10)
    part1 = get_covered_ground(elves)
    part2 = 10 + spread(elves, 2_000)

    return part1, part2


def main() -> None:
    import os

    res = solve(os.path.dirname(os.path.abspath(__file__)) + "/input.txt")

    assert res[0] == 4005, f"Part1 = {res[0]}"
    assert res[1] == 1008, f"Part2 = {res[1]}"


if __name__ == "__main__":
    main()
