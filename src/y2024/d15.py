# Advent of Code : Day 15 - Warehouse Woes
# https://adventofcode.com/2024/day/15

from helpers import Timer, load_input_data

DIRS = {"^": -1 + 0j, ">": 0 + 1j, "v": 1 + 0j, "<": 0 - 1j}


@Timer.timeit
def simulate_robot_moves(warehouse: dict[complex, str], moves: str) -> None:
    def is_moveable(z: complex, dir: complex) -> bool:
        z += dir
        return any(
            (
                warehouse[z] == ".",
                warehouse[z] == "O" and is_moveable(z, dir),
                warehouse[z] == "["
                and (
                    is_moveable(z + DIRS[">"], dir)
                    and (is_moveable(z, dir) if dir != DIRS[">"] else True)
                ),
                warehouse[z] == "]"
                and (
                    is_moveable(z + DIRS["<"], dir)
                    and (is_moveable(z, dir) if dir != DIRS["<"] else True)
                ),
            )
        )

    def push(z: complex, dir: complex) -> None:
        z += dir
        if warehouse[z] == "[":
            push(z + DIRS[">"], dir)
        elif warehouse[z] == "]":
            push(z + DIRS["<"], dir)

        if warehouse[z] != ".":
            push(z, dir)
        warehouse[z], warehouse[z - dir] = warehouse[z - dir], warehouse[z]

    curr = next(k for k, v in warehouse.items() if v == "@")
    for move in moves:
        dir = DIRS[move]

        if is_moveable(curr, dir):
            push(curr, dir)
            curr += dir


@Timer.timeit
def sum_boxes_GPS_coordinates(warehouse: dict[complex, str]) -> int:
    ans = sum(k for k, v in warehouse.items() if v in "O[")
    return int(100 * ans.real + ans.imag)


@Timer.timeit
def parse(data: str) -> tuple[dict[complex, str], dict[complex, str], str]:
    grid1, moves = data.split("\n\n")
    grid2 = grid1.translate(str.maketrans({"#": "##", ".": "..", "O": "[]", "@": "@."}))

    warehouse1, warehouse2 = (
        {
            complex(i, j): col
            for i, row in enumerate(grid.splitlines())
            for j, col in enumerate(row)
        }
        for grid in (grid1, grid2)
    )

    return warehouse1, warehouse2, moves.replace("\n", "")


@Timer.timeit
def solve(data: str) -> tuple[int, int]:
    warehouse1, warehouse2, moves = parse(data)
    simulate_robot_moves(warehouse1, moves)
    simulate_robot_moves(warehouse2, moves)
    part1 = sum_boxes_GPS_coordinates(warehouse1)
    part2 = sum_boxes_GPS_coordinates(warehouse2)

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2024, 15)))
