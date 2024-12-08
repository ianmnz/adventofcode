# Advent of Code : Day 08 - Resonant Collinearity
# https://adventofcode.com/2024/day/08


from collections import defaultdict

from helpers import Timer, load_input_data


@Timer.timeit
def get_nb_uniq_antinodes(antennas: list[list[str]]) -> tuple[int, int]:
    m = len(antennas)
    n = len(antennas[0])

    def is_valid(z: complex) -> bool:
        return 0 <= z.real < m and 0 <= z.imag < n

    freq: dict[str, list[complex]] = defaultdict(list)
    antinodes = set()
    antinodes_resonant_harmonics = set()

    for i, row in enumerate(antennas):
        for j, col in enumerate(row):
            if col == ".":
                continue

            curr = complex(i, j)

            for prev in freq[col]:
                diff = curr - prev
                antinode1 = curr + diff
                antinode2 = prev - diff

                # Part1
                if is_valid(antinode1):
                    antinodes.add(antinode1)

                if is_valid(antinode2):
                    antinodes.add(antinode2)

                # Part 2
                antinodes_resonant_harmonics |= {curr, prev}

                while is_valid(antinode1):
                    antinodes_resonant_harmonics.add(antinode1)
                    antinode1 += diff

                while is_valid(antinode2):
                    antinodes_resonant_harmonics.add(antinode2)
                    antinode2 -= diff

            freq[col].append(curr)

    return len(antinodes), len(antinodes_resonant_harmonics)


@Timer.timeit
def parse(data: str) -> list[list[str]]:
    return [[c for c in line] for line in data.splitlines()]


@Timer.timeit
def solve(data: str) -> tuple[int, int]:
    antennas = parse(data)
    part1, part2 = get_nb_uniq_antinodes(antennas)

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2024, 8)))
