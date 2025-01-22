# Advent of Code : Day 10 - Cathode-Ray Tube
# https://adventofcode.com/2022/day/10


from helpers import Timer, load_input_data

CYCLES_PER_INSTRUCTION = {"noop": 1, "addx": 2}

CYCLES_OF_INTEREST = [20, 60, 100, 140, 180, 220]

CRT_WIDTH = 40
CRT_HEIGHT = 6
SPRITE_WIDTH = 3


@Timer.timeit
def get_CRT_signals_and_display(
    program: list[list[str]],
) -> tuple[int, list[list[str]]]:
    sum_signal_strength_on_cycles_of_interest = 0
    crt = [["." for _ in range(CRT_WIDTH)] for _ in range(CRT_HEIGHT)]

    cycle_counter = 1
    register = 1
    for instruction in program:
        for cycle in range(CYCLES_PER_INSTRUCTION.get(instruction[0], 0)):
            if cycle_counter in CYCLES_OF_INTEREST:
                sum_signal_strength_on_cycles_of_interest += cycle_counter * register

            i, j = divmod(cycle_counter - 1, CRT_WIDTH)

            if abs(register - j) <= (SPRITE_WIDTH // 2):
                crt[i][j] = "#"

            if instruction[0] == "addx" and cycle + 1 == CYCLES_PER_INSTRUCTION["addx"]:
                register += int(instruction[1])

            cycle_counter += 1

    return sum_signal_strength_on_cycles_of_interest, crt


def display_crt(crt: list[list[str]]) -> str:
    # for i in range(CRT_HEIGHT):
    #     for j in range(CRT_WIDTH):
    #         print(crt[i][j], end="")
    #     print()
    return "EFUGLPAP"  # It should print this


@Timer.timeit
def parse(data: str) -> list[list[str]]:
    return [instruction.strip().split() for instruction in data.strip().split("\n")]


@Timer.timeit
def solve(data: str) -> tuple[int, str]:
    program = parse(data)
    part1, crt = get_CRT_signals_and_display(program)
    part2 = display_crt(crt)

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2022, 10)))
