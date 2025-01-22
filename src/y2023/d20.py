# Advent of Code : Day 20 - Pulse Propagation
# https://adventofcode.com/2023/day/20

import math
from collections import deque

from helpers import Timer, load_input_data

adjacency = {}
flipflops = {}
conjunctions = {}
parent_conjunction_nb_presses = {}
conj_parent = ""


@Timer.timeit
def build_graph(configuration: list[list[str]], target: str = "rx") -> None:
    adjacency.clear()
    flipflops.clear()
    conjunctions.clear()

    for sender, receivers in configuration:
        if sender[0] == "%":
            sender = sender[1:]
            flipflops[sender] = False

        elif sender[0] == "&":
            sender = sender[1:]
            conjunctions[sender] = dict()

        adjacency[sender] = receivers.split(", ")

    for sender, receivers in adjacency.items():
        for receiver in receivers:
            if receiver == target:
                global conj_parent
                conj_parent = sender

            if receiver in conjunctions:
                conjunctions[receiver][sender] = False


def press(counter: int = 1) -> tuple[int]:
    nb_low_pulses, nb_high_pulses = 1, 0

    queue = deque()
    for receiver in adjacency["broadcaster"]:
        nb_low_pulses += 1
        queue.append(("broadcaster", False, receiver))

    while queue:
        sender, is_pulse_received_high, receiver = queue.popleft()

        is_pulse_sent_high = False

        if receiver in conjunctions:
            conjunctions[receiver][sender] = is_pulse_received_high
            if any(
                not is_pulse_high for is_pulse_high in conjunctions[receiver].values()
            ):
                is_pulse_sent_high = True

        elif receiver in flipflops:
            if is_pulse_received_high:
                continue
            else:
                flipflops[receiver] = not flipflops[receiver]
                is_pulse_sent_high = flipflops[receiver]

        for destination in adjacency.get(receiver, []):
            if is_pulse_sent_high:
                nb_high_pulses += 1
            else:
                nb_low_pulses += 1
            queue.append((receiver, is_pulse_sent_high, destination))

        for sender, nb_presses in parent_conjunction_nb_presses.items():
            if conjunctions[conj_parent][sender] and nb_presses < 0:
                parent_conjunction_nb_presses[sender] = counter

    return nb_low_pulses, nb_high_pulses


@Timer.timeit
def prod_low_high_pulses(nb_presses: int = 1000) -> int:
    low, high = 0, 0
    for _ in range(nb_presses):
        l, h = press()
        low += l
        high += h
    return low * high


@Timer.timeit
def get_fewest_nb_presses() -> int:
    for sender in conjunctions[conj_parent]:
        parent_conjunction_nb_presses[sender] = -1

    count = 1
    while any(nb_presses < 0 for nb_presses in parent_conjunction_nb_presses.values()):
        press(count)
        count += 1

    lcm = 1
    for val in parent_conjunction_nb_presses.values():
        lcm = (lcm * val) // math.gcd(lcm, val)
    return lcm


@Timer.timeit
def parse(data: str) -> list[list[str]]:
    configuration = [line.split(" -> ") for line in data.split("\n")]
    return configuration


@Timer.timeit
def solve(data: str) -> tuple[int, int]:
    configuration = parse(data)
    build_graph(configuration)

    part1 = prod_low_high_pulses()

    build_graph(configuration)
    part2 = get_fewest_nb_presses()

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2023, 20)))
