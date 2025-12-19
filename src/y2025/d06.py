# Advent of Code : Day 06 - Trash Compactor
# https://adventofcode.com/2025/day/6

import operator
from functools import reduce

from helpers import Timer, load_input_data


def solve_total_human(raw_homework: list[str]) -> int:
    # Split homework into its numbers
    # Except for the last row which stores the operation
    homework = [row.split() for row in raw_homework]

    def solve_col(j: int) -> int:
        return reduce(
            operator.mul if homework[-1][j] == "*" else operator.add,
            (int(row[j]) for row in homework[:-1]),
        )

    return sum(solve_col(j) for j in range(len(homework[0])))


def solve_total_cephalopod(raw_homework: list[str]) -> int:
    res = 0

    # We split each string into its characters
    # Then we transpose the resulting matrix
    for it in zip(*(tuple(row_str) for row_str in raw_homework)):
        col = "".join(it).strip()

        if not col:
            # End of section of columns in the original homework
            # We gather the previous computation
            res += reduce(operation, operands)

        elif col[-1] in "*+":
            # New section of columns in the original homework
            # We identify the corresponding operation
            # And insert first operand
            operation = operator.mul if col[-1] == "*" else operator.add
            operands = [int(col[:-1])]

        else:
            # We are inside a section of columns in the original homework
            # Just add the current operand
            operands.append(int(col))

    # Must account for last section
    return res + reduce(operation, operands)


@Timer.timeit
def parse(data: str) -> list[str]:
    return data.split("\n")


@Timer.timeit
def solve(data: str) -> tuple[int, int]:
    raw_homework = parse(data)
    part1 = solve_total_human(raw_homework)
    part2 = solve_total_cephalopod(raw_homework)

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2025, 6)))
