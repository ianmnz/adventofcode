# Advent of Code : Day 17 - Chronospatial Computer
# https://adventofcode.com/2024/day/17

import re

from helpers import Timer, load_input_data


def run(a: int, b: int, c: int, prog: list[int]) -> list[int]:
    ans = []
    iptr = 0
    n = len(prog)

    while iptr < n:
        opcode, operand = prog[iptr], prog[iptr + 1]
        combo = operand if operand < 4 else [a, b, c][operand - 4]

        match opcode:
            case 0:  # adv
                a >>= combo
            case 1:  # bxl
                b ^= operand
            case 2:  # bst
                b = combo & 7  # => combo % 8
            case 3:  # jnz
                iptr = operand - 2 if a else iptr
            case 4:  # bxc
                b ^= c
            case 5:  # out
                ans.append(combo & 7)
            case 6:  # bdv
                b = a >> combo
            case 7:  # cdv
                c = a >> combo

        iptr += 2

    return ans


def _find_a(prog: list[int], prog_ptr: int, a: int) -> int:
    if prog_ptr < 0:
        return a

    for r in range(8):
        if run(a * 8 + r, 0, 0, prog) == prog[prog_ptr:]:
            if (ret := _find_a(prog, prog_ptr - 1, a * 8 + r)) >= 0:
                return ret
    return -1


@Timer.timeit
def display(a: int, b: int, c: int, prog: list[int]) -> str:
    return ",".join(map(str, run(a, b, c, prog)))


@Timer.timeit
def find_a(prog: list[int]) -> int:
    """
    Based on:
    https://www.reddit.com/r/adventofcode/comments/1hg38ah/comment/m2k2ka5/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
    https://www.reddit.com/r/adventofcode/comments/1hg38ah/comment/m2hmgw5/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
    https://www.reddit.com/r/adventofcode/comments/1hg38ah/comment/m2ggd01/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button

    We backtrack recursively until find the proper A
    Since the program finishes when A == 0, we start there.
    B and C are set from A each iteration, so we can ignore both of
    them and define them as zero.
    """
    return _find_a(prog, len(prog) - 1, 0)


@Timer.timeit
def parse(data: str) -> tuple[int, int, int, list[int]]:
    a, b, c, *prog = map(int, re.findall(r"\d+", data))
    return a, b, c, prog


@Timer.timeit
def solve(data: str) -> tuple[str, int]:
    a, b, c, prog = parse(data)
    part1 = display(a, b, c, prog)
    part2 = find_a(prog)

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2024, 17)))
