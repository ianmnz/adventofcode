# Advent of Code : Day 09 - Mirage Maintenance
# https://adventofcode.com/2023/day/9


from helpers import Timer, load_input_data


def extrapolate(history: list[int]) -> int:
    deltas = [t - t_1 for t_1, t in zip(history, history[1:])]
    return history[-1] + extrapolate(deltas) if any(t != 0 for t in history) else 0


@Timer.timeit
def parse(data: str) -> list[list[int]]:
    return [[*map(int, line.split())] for line in data.splitlines()]


@Timer.timeit
def solve(data: str) -> tuple[int, int]:
    histories = parse(data)
    part1 = sum([extrapolate(history) for history in histories])
    part2 = sum([extrapolate(history[::-1]) for history in histories])

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2023, 9)))
