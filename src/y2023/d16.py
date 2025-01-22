# Advent of Code : Day 16 - The Floor Will Be Lava
# https://adventofcode.com/2023/day/16

from dataclasses import dataclass

from helpers import Timer, load_input_data


@dataclass
class Beam:
    start: tuple[int, int]
    dir: tuple[int, int]

    def __hash__(self) -> int:
        return hash((*self.start, *self.dir))


def propagate_beams(
    layout: list[list[str]], starting_beam: Beam = Beam((0, -1), (0, 1))
) -> list[list[int]]:
    n = len(layout)
    m = len(layout[0])

    energized = [[0 for _ in range(m)] for _ in range(n)]

    stack = [starting_beam]
    visited = set()

    while stack:
        beam = stack.pop()

        if beam in visited:
            continue

        visited.add(beam)

        pos_i, pos_j = beam.start
        dir_i, dir_j = beam.dir

        while (0 <= pos_i + dir_i < n) and (0 <= pos_j + dir_j < m):
            pos_i += dir_i
            pos_j += dir_j

            energized[pos_i][pos_j] = 1

            if layout[pos_i][pos_j] == "/":
                stack.append(Beam((pos_i, pos_j), (-dir_j, -dir_i)))
                break

            elif layout[pos_i][pos_j] == "\\":
                stack.append(Beam((pos_i, pos_j), (dir_j, dir_i)))
                break

            elif layout[pos_i][pos_j] == "|" and dir_j != 0:  # Horizontal beam
                stack.append(Beam((pos_i, pos_j), (-1, 0)))
                stack.append(Beam((pos_i, pos_j), (1, 0)))
                break

            elif layout[pos_i][pos_j] == "-" and dir_i != 0:  # Vertical beam
                stack.append(Beam((pos_i, pos_j), (0, -1)))
                stack.append(Beam((pos_i, pos_j), (0, 1)))
                break

    return energized


def count_energized_tiles(energized: list[list[int]]) -> int:
    return sum(mask for row in energized for mask in row)


@Timer.timeit
def find_best_starting_beam(layout: list[list[str]]) -> int:
    n = len(layout)
    m = len(layout[0])

    most_energized = 0

    for j in range(m):
        top = count_energized_tiles(
            propagate_beams(layout, Beam((-1, j), (1, 0)))
        )  # Top row
        bottom = count_energized_tiles(
            propagate_beams(layout, Beam((n, j), (-1, 0)))
        )  # Bottom row
        most_energized = max([most_energized, top, bottom])

    for i in range(m):
        left = count_energized_tiles(
            propagate_beams(layout, Beam((i, -1), (0, 1)))
        )  # Leftmost column
        right = count_energized_tiles(
            propagate_beams(layout, Beam((i, m), (0, -1)))
        )  # Rightmost column
        most_energized = max([most_energized, left, right])

    return most_energized


@Timer.timeit
def parse(data: str) -> list[list[str]]:
    return [[char for char in line] for line in data.split("\n")]


@Timer.timeit
def solve(data: str) -> tuple[int, int]:
    layout = parse(data)
    part1 = count_energized_tiles(propagate_beams(layout))
    part2 = find_best_starting_beam(layout)

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2023, 16)))
