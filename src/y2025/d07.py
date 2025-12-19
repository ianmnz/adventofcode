# Advent of Code : Day 07 - Laboratories
# https://adventofcode.com/2025/day/7

from helpers import Timer, load_input_data


def simulate_beams(diagram: list[list[int]]) -> tuple[int, int]:
    # Some (fair) assumptions about the data:
    #  * There are no splitters ('^') in the last line;
    #  * There are no horizontally adjacent splitters ('^');
    #  * There are no diagonally adjacent splitters ('^');
    #  * There is enough padding on both sides to avoid checking bounds;
    nb_splits = 0
    for i, row in enumerate(diagram[:-1]):
        for j, col in enumerate(row):
            if col <= 0:
                # Column is not a beam
                continue

            if diagram[i + 1][j] < 0:
                # Cell below is a splitter
                nb_splits += 1
                diagram[i + 1][j - 1] += col
                diagram[i + 1][j + 1] += col

            else:
                # Cell below is either empty or another beam
                diagram[i + 1][j] += col

    return nb_splits, sum(diagram[-1])


@Timer.timeit
def parse(data: str) -> list[list[int]]:
    char2int = {"^": -1, ".": 0, "S": 1}
    return [[char2int[col] for col in row] for row in data.split("\n")]


@Timer.timeit
def solve(data: str) -> tuple[int, int]:
    diagram = parse(data)
    part1, part2 = simulate_beams(diagram)

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2025, 7)))
