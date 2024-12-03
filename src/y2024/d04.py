# Advent of Code : Day 04 - Ceres Search
# https://adventofcode.com/2024/day/04

from helpers import Timer, load_input_data


@Timer.timeit
def add_padding(puzzle: list[str], pad: int, char: str = "*") -> list[str]:
    n = len(puzzle[0])
    pad_row: str = char * (n + 2 * pad)
    pad_col: str = char * pad
    return (
        [pad_row] * pad + [pad_col + row + pad_col for row in puzzle] + [pad_row] * pad
    )


@Timer.timeit
def searchXMAS(puzzle: list[str]) -> int:
    pattern = "XMAS"
    pad = len(pattern) - 1
    padded = add_padding(puzzle, pad)

    def substr(pos: tuple[int, int], dir: tuple[int, int]) -> str:
        x, y = pos
        dx, dy = dir
        return "".join([padded[x + i * dx][y + i * dy] for i in range(len(pattern))])

    count = 0
    for i in range(pad, len(puzzle) + pad):
        for j in range(pad, len(puzzle[0]) + pad):
            if padded[i][j] != "X":
                continue

            pos = (i, j)

            count += substr(pos, (0, +1)) == pattern  # horizontal right
            count += substr(pos, (0, -1)) == pattern  # horizontal left

            count += substr(pos, (+1, 0)) == pattern  # vertical down
            count += substr(pos, (-1, 0)) == pattern  # vertical up

            count += substr(pos, (+1, +1)) == pattern  # main diagonal down
            count += substr(pos, (-1, -1)) == pattern  # main diagonal up

            count += substr(pos, (-1, +1)) == pattern  # anti diagonal up
            count += substr(pos, (+1, -1)) == pattern  # anti diagonal down

    return count


@Timer.timeit
def searchX_MAS(puzzle: list[str]) -> int:
    # Rotate patterns for the corners
    patterns = ["MSSM", "SSMM", "SMMS", "MMSS"]
    pad = 1
    padded = add_padding(puzzle, pad)

    count = 0
    for i in range(pad, len(puzzle) + pad):
        for j in range(pad, len(puzzle[0]) + pad):
            if padded[i][j] != "A":
                continue

            corners = "".join(
                [
                    padded[i - 1][j - 1],  # top-left
                    padded[i - 1][j + 1],  # top-right
                    padded[i + 1][j + 1],  # bottom-right
                    padded[i + 1][j - 1],  # bottom-left
                ]
            )

            count += corners in patterns

    return count


@Timer.timeit
def parse(data: str) -> list[str]:
    return data.splitlines()


@Timer.timeit
def solve(data: str) -> tuple[int, int]:
    puzzle = parse(data)
    part1 = searchXMAS(puzzle)
    part2 = searchX_MAS(puzzle)

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2024, 4)))
