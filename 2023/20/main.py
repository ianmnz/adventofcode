# Advent of Code : Day 20 - Pulse Propagation
# https://adventofcode.com/2023/day/20

import math
from typing import List, Tuple
from collections import deque


adjacency = {}
flipflops = {}
conjunctions = {}
parent_conjunction_nb_presses = {}
conj_parent = ''


def build_graph(configuration: List[List[str]], target: str = 'rx') -> None:
    adjacency.clear()
    flipflops.clear()
    conjunctions.clear()

    for sender, receivers in configuration:
        if sender[0] == '%':
            sender = sender[1:]
            flipflops[sender] = False

        elif sender[0] == '&':
            sender = sender[1:]
            conjunctions[sender] = dict()

        adjacency[sender] = receivers.split(', ')

    for sender, receivers in adjacency.items():
        for receiver in receivers:
            if receiver == target:
                global conj_parent
                conj_parent = sender

            if receiver in conjunctions:
                conjunctions[receiver][sender] = False


def press(counter: int = 1) -> Tuple[int]:
    nb_low_pulses, nb_high_pulses = 1, 0

    queue = deque()
    for receiver in adjacency['broadcaster']:
        nb_low_pulses += 1
        queue.append(("broadcaster", False, receiver))

    while queue:
        sender, is_pulse_received_high, receiver = queue.popleft()

        is_pulse_sent_high = False

        if receiver in conjunctions:
            conjunctions[receiver][sender] = is_pulse_received_high
            if any(not is_pulse_high for is_pulse_high in conjunctions[receiver].values()):
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


def prod_low_high_pulses(nb_presses: int = 1000) -> int:
    low, high = 0, 0
    for _ in range(nb_presses):
        l, h = press()
        low += l
        high += h
    return low * high


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


def main():
    import os
    import sys

    # To be able to import the helpers module
    sys.path.append(os.path.dirname(                                        # Project
                        os.path.dirname(                                    # Year
                            os.path.dirname(os.path.abspath(__file__)))))   # Day

    from helpers import Timer

    with open("input.txt", "r") as file:
        configuration = [line.split(' -> ') for line in file.read().split('\n')]

    # --- Part 1 --- #
    with Timer():
        build_graph(configuration)
        print("Product of total low and high pulses sent:", prod_low_high_pulses())  # 873301506

    # --- Part 2 --- #
    with Timer():
        build_graph(configuration)
        print("Fewest number of button presses required to send a low pulse to 'rx':",
              get_fewest_nb_presses())  # 241823802412393


if __name__ == "__main__":
    main()
