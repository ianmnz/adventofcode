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

    def count(pos: tuple[int, int]) -> int:
        found = 0
        found += substr(pos, (0, +1)) == pattern  # horizontal right
        found += substr(pos, (0, -1)) == pattern  # horizontal left

        found += substr(pos, (+1, 0)) == pattern  # vertical down
        found += substr(pos, (-1, 0)) == pattern  # vertical up

        found += substr(pos, (+1, +1)) == pattern  # main diagonal down
        found += substr(pos, (-1, -1)) == pattern  # main diagonal up

        found += substr(pos, (-1, +1)) == pattern  # anti diagonal up
        found += substr(pos, (+1, -1)) == pattern  # anti diagonal down
        return found

    return sum(
        map(
            count,
            filter(
                lambda pos: padded[pos[0]][pos[1]] == "X",
                (
                    (i, j)
                    for i in range(pad, len(puzzle) + pad)
                    for j in range(pad, len(puzzle[0]) + pad)
                ),
            ),
        )
    )


@Timer.timeit
def searchX_MAS(puzzle: list[str]) -> int:
    # Rotate patterns for the corners
    patterns = ["MSSM", "SSMM", "SMMS", "MMSS"]

    def count(pos: tuple[int, int]) -> int:
        i, j = pos
        corners = "".join(
            [
                puzzle[i - 1][j - 1],  # top-left
                puzzle[i - 1][j + 1],  # top-right
                puzzle[i + 1][j + 1],  # bottom-right
                puzzle[i + 1][j - 1],  # bottom-left
            ]
        )
        return int(corners in patterns)

    return sum(
        map(
            count,
            filter(
                lambda pos: puzzle[pos[0]][pos[1]] == "A",
                (
                    (i, j)
                    for i in range(1, len(puzzle) - 1)
                    for j in range(1, len(puzzle[0]) - 1)
                ),
            ),
        )
    )


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
