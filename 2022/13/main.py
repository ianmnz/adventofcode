# Advent of Code : Day 13 - Distress Signal
# https://adventofcode.com/2022/day/13

import bisect
from dataclasses import dataclass
from functools import reduce
from typing import List, Tuple, Union

from helpers import Timer

Value = List[Union[int, "Value"]]


@dataclass(frozen=True)
class PacketWrapper:
    """
    Wrapper to be able to use sorted()
    and bisect.bisect() by using the
    dunder method __lt__
    """

    value: Value

    def __lt__(self, other: "PacketWrapper") -> bool:
        return compare(self.value, other.value)


def compare(l_packet: Value, r_packet: Value) -> bool:
    if l_packet == r_packet:
        return True

    for lhs, rhs in zip(l_packet, r_packet):
        if lhs == rhs:
            continue

        if isinstance(lhs, int) and isinstance(rhs, int):
            return lhs < rhs

        elif isinstance(lhs, int) and isinstance(rhs, list):
            return compare([lhs], rhs)

        elif isinstance(lhs, list) and isinstance(rhs, int):
            return compare(lhs, [rhs])

        elif isinstance(lhs, list) and isinstance(rhs, list):
            return compare(lhs, rhs)

    return len(l_packet) <= len(r_packet)


@Timer.timeit
def get_sum_of_indices(packets: List[Tuple[Value, Value]]) -> int:
    return sum(
        idx for idx, (lhs, rhs) in enumerate(packets, start=1) if compare(lhs, rhs)
    )


@Timer.timeit
def get_distress_signal_decoder_key(
    packets: List[Tuple[Value, Value]], dividers: List[Value] = [[[2]], [[6]]]
) -> int:
    wrappers = []
    for lhs, rhs in packets:
        wrappers.extend([PacketWrapper(lhs), PacketWrapper(rhs)])
    wrapped_dividers = [PacketWrapper(divider) for divider in dividers]

    wrappers = sorted(wrappers + wrapped_dividers)
    return reduce(
        lambda x, y: x * y,
        [(bisect.bisect(wrappers, divider) + 1) for divider in wrapped_dividers],
    )


@Timer.timeit
def parse(filename: str) -> List[Tuple[Value, Value]]:
    with open(filename, "r") as file:
        packets = [
            tuple(map(eval, pair.split("\n")))
            for pair in file.read().strip().split("\n\n")
        ]
    return packets


@Timer.timeit
def solve(filename: str) -> Tuple[int, int]:
    packets = parse(filename)
    part1 = get_sum_of_indices(packets)
    part2 = get_distress_signal_decoder_key(packets)

    return part1, part2


def main() -> None:
    import os

    res = solve(os.path.dirname(os.path.abspath(__file__)) + "/input.txt")

    assert res[0] == 5825, f"Part1 = {res[0]}"
    assert res[1] == 24477, f"Part2 = {res[1]}"


if __name__ == "__main__":
    main()
