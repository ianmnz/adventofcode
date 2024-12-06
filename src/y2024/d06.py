# Advent of Code : Day 06 - Guard Gallivant
# https://adventofcode.com/2024/day/06

from helpers import Timer, load_input_data


@Timer.timeit
def get_starting_point(grid: list[list[str]]) -> complex:
    for i, row in enumerate(grid):
        for j, col in enumerate(row):
            if col == "^":
                return complex(i, j)
    return 0j


def simulate_guard_path(
    grid: list[list[str]], start: complex
) -> tuple[set[tuple[complex, complex]], bool]:
    m = len(grid)
    n = len(grid[0])

    def is_valid(z: complex) -> bool:
        return (0 <= z.real < m) and (0 <= z.imag < n)

    curr = start
    dir = -1  # -1, 1j, 1, -1j
    visited: set[tuple[complex, complex]] = set()

    while is_valid(curr) and (curr, dir) not in visited:
        visited.add((curr, dir))

        next = curr + dir

        if is_valid(next) and grid[int(next.real)][int(next.imag)] in "#O":
            dir *= -1j  # Rotate -90o

        else:
            curr = next

    return visited, (curr, dir) in visited


@Timer.timeit
def get_guard_path(grid: list[list[str]], start: complex) -> set[complex]:
    visited = simulate_guard_path(grid, start)[0]
    return {pos for pos, _ in visited}


@Timer.timeit
def count_nb_possible_obstructions(
    grid: list[list[str]], start: complex, path: set[complex]
) -> int:
    count = 0
    for pos in path:
        i, j = map(int, (pos.real, pos.imag))
        cached, grid[i][j] = grid[i][j], "O"

        count += simulate_guard_path(grid, start)[1]

        grid[i][j] = cached
    return count


@Timer.timeit
def parse(data: str) -> list[list[str]]:
    return [[col for col in row] for row in data.splitlines()]


@Timer.timeit
def solve(data: str) -> tuple[int, int]:
    grid = parse(data)
    start = get_starting_point(grid)
    path = get_guard_path(grid, start)
    part1 = len(path)
    part2 = count_nb_possible_obstructions(grid, start, path)

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2024, 6)))
