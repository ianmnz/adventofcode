# Advent of Code : Day 24 - Crossed Wires
# https://adventofcode.com/2024/day/24

from helpers import Timer, load_input_data


@Timer.timeit
def propagate(wires: dict[str, int], gates: dict[str, tuple[str, str, str]]) -> int:
    def evaluate(out) -> int:
        if out in wires:
            return wires[out]

        in1, op, in2 = gates[out]
        match op:
            case "AND":
                wires[out] = evaluate(in1) & evaluate(in2)
            case "OR":
                wires[out] = evaluate(in1) | evaluate(in2)
            case "XOR":
                wires[out] = evaluate(in1) ^ evaluate(in2)

        return wires[out]

    return sum(
        (1 << i) * bit
        for i, bit in enumerate(
            (evaluate(z) for z in sorted(wire for wire in gates if wire[0] == "z"))
        )
    )


@Timer.timeit
def find_swapped_gates(gates: dict[str, tuple[str, str, str]]) -> str:
    # Based on:
    # https://www.reddit.com/r/adventofcode/comments/1hl698z/comment/m3k68gd/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
    # https://www.reddit.com/r/adventofcode/comments/1hl698z/comment/m3kt1je/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button

    final_carry_z = max(wire for wire in gates if wire[0] == "z")

    wrong = set()
    for out, (in1, op, in2) in gates.items():
        if out[0] == "z" and op != "XOR" and out != final_carry_z:
            wrong.add(out)

        if op == "XOR" and all(wire[0] not in "xyz" for wire in (out, in1, in2)):
            wrong.add(out)

        if op == "AND" and "x00" not in (in1, in2):
            for in12, op2, in22 in gates.values():
                if (out == in12 or out == in22) and op2 != "OR":
                    wrong.add(out)
                    break

        if op == "XOR":
            for in12, op2, in22 in gates.values():
                if (out == in12 or out == in22) and op2 == "OR":
                    wrong.add(out)
                    break

    return ",".join(sorted(wrong))


@Timer.timeit
def parse(data: str) -> tuple[dict[str, int], dict[str, tuple[str, str, str]]]:
    top, bottom = data.split("\n\n")

    wires = {}
    for input in top.splitlines():
        wire, val = input.split(": ")
        wires[wire] = int(val)

    gates = {}
    for gate in bottom.splitlines():
        in1, op, in2, _, out = gate.split(" ")
        gates[out] = (in1, op, in2)

    return wires, gates


@Timer.timeit
def solve(data: str) -> tuple[int, str]:
    wires, gates = parse(data)
    part1 = propagate(wires, gates)
    part2 = find_swapped_gates(gates)

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2024, 24)))
