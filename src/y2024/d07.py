# Advent of Code : Day 07 - Bridge Repair
# https://adventofcode.com/2024/day/07

from helpers import Timer, load_input_data


def check_equation(target: int, factors: list[int], with_concat: bool) -> bool:
    acc = factors[0]
    index = 1
    stack: list[tuple[int, int]] = [(acc, index)]

    while stack:
        acc, index = stack.pop()

        if index >= len(factors):
            if target == acc:
                return True
            continue

        factor = factors[index]
        index += 1

        if (summation := acc + factor) <= target:
            stack.append((summation, index))

        if (product := acc * factor) <= target:
            stack.append((product, index))

        if with_concat:
            if (concatenation := int(f"{acc}{factor}")) <= target:
                stack.append((concatenation, index))

    return False


@Timer.timeit
def get_total_calibration(equations) -> tuple[int, int]:
    total_without_concat = 0
    total_with_concat = 0

    for target, factors in equations:
        if check_equation(target, factors, False):
            total_without_concat += target

        elif check_equation(target, factors, True):
            total_with_concat += target

    return total_without_concat, total_without_concat + total_with_concat


@Timer.timeit
def parse(data: str) -> list[tuple[int, list[int]]]:
    equations = []
    for equation in data.splitlines():
        target, factors = equation.split(": ")
        equations.append((int(target), [int(n) for n in factors.split(" ")]))
    return equations


@Timer.timeit
def solve(data: str) -> tuple[int, int]:
    equations = parse(data)
    part1, part2 = get_total_calibration(equations)

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2024, 7)))
