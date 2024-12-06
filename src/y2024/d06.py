# Advent of Code : Day 06 - Guard Gallivant
# https://adventofcode.com/2024/day/06

from helpers import Timer, load_input_data

type Pos = tuple[complex, complex]
type Path = dict[Pos, int]


def is_valid(z: complex, m: int, n: int) -> bool:
    return (0 <= z.real < m) and (0 <= z.imag < n)


@Timer.timeit
def get_starting_point(grid: list[list[str]]) -> complex:
    for i, row in enumerate(grid):
        for j, col in enumerate(row):
            if col == "^":
                return complex(i, j)
    return 0j


def simulate_guard_path(
    grid: list[list[str]], pos0: complex, dir0: complex = -1 + 0j
) -> tuple[Path, bool]:
    m = len(grid)
    n = len(grid[0])

    curr = pos0
    dir = dir0  # -1, 1j, 1, -1j
    path: Path = {}
    step = 0

    while is_valid(curr, m, n) and not (cycled := (curr, dir) in path):
        step += 1
        path[(curr, dir)] = step

        next = curr + dir

        if is_valid(next, m, n) and grid[int(next.real)][int(next.imag)] in "#O":
            dir *= -1j  # Rotate -90o

        else:
            curr = next

    return path, cycled


@Timer.timeit
def get_guard_path(grid: list[list[str]], start: complex) -> tuple[set[complex], Path]:
    path = simulate_guard_path(grid, start)[0]
    return {pos for pos, _ in path}, path


@Timer.timeit
def count_idx_possible_obstructions(grid: list[list[str]], path: Path) -> int:
    m = len(grid)
    n = len(grid[0])

    # The goal here is to check if putting an obstacle
    # in the next position creates a cycle.
    count = 0
    for (pos, dir), step in path.items():
        next = pos + dir

        # We can only put an obstacle in a place where we did haven't
        # passed yet, i.e., our current step must be smaller than
        # any step where we passed through this point
        if any(
            (visited := path.get((next, d))) and visited < step
            for d in (-1 + 0j, 1j, 1 + 0j, -1j)
        ):
            continue

        i, j = map(int, (next.real, next.imag))

        if is_valid(next, m, n) and grid[i][j] != "#":
            cached, grid[i][j] = grid[i][j], "O"

            count += simulate_guard_path(grid, pos, dir)[1]

            grid[i][j] = cached

    return count


@Timer.timeit
def parse(data: str) -> list[list[str]]:
    return [[col for col in row] for row in data.splitlines()]


@Timer.timeit
def solve(data: str) -> tuple[int, int]:
    grid = parse(data)
    start = get_starting_point(grid)
    visited, path = get_guard_path(grid, start)
    part1 = len(visited)
    part2 = count_idx_possible_obstructions(grid, path)

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2024, 6)))
