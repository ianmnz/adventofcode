# Advent of Code : Day 16 - Proboscidea Volcanium
# https://adventofcode.com/2022/day/16

import os
import re
from dataclasses import dataclass
from functools import lru_cache
from typing import Dict, List, Tuple

from helpers import Timer


@dataclass
class Valve:
    label: str
    flow: int
    tunnels: Dict[str, int]


@Timer.timeit
def floyd_warshall(valves: Dict[str, Valve]) -> None:
    INF = 99999

    for k, valve_k in valves.items():
        for valve_i in valves.values():
            for j in valves.keys():
                valve_i.tunnels[j] = min(
                    valve_i.tunnels.get(j, INF),
                    valve_i.tunnels.get(k, INF) + valve_k.tunnels.get(j, INF),
                )


@Timer.timeit
def filter_functioning_valves(valves: Dict[str, Valve], start: str) -> None:
    valves_to_remove = []

    for label, valve in valves.items():
        del valve.tunnels[label]

        if (valve.flow <= 0) and (label != start):
            for adj in valve.tunnels:
                del valves[adj].tunnels[label]
            valves_to_remove.append(label)

    for label in valves_to_remove:
        del valves[label]


@Timer.timeit
def build_graph(report: List[str], start: str = "AA") -> Dict[str, Valve]:
    valves = {}

    pattern = re.compile(
        r"Valve (\w+) has flow rate=(\d+); tunnel[s]? lead[s]? to valve[s]? (\w+(?:, \w+)*)$"
    )
    for line in report:
        match = pattern.match(line)
        if match is not None:
            label = match.group(1)
            flow = int(match.group(2))
            tunnels = {adj: 1 for adj in match.group(3).split(", ")}

            valves[label] = Valve(label, flow, tunnels)

    floyd_warshall(valves)
    filter_functioning_valves(valves, start)

    return valves


@Timer.timeit
def maximize_released_pressure(
    valves: Dict[str, Valve], total_time: int, with_help: bool, start: str = "AA"
) -> int:
    mask = {label: 1 << i for i, label in enumerate(valves)}

    @lru_cache(maxsize=None)
    def search(curr: str, opened: int, t_left: int, in_parallel: bool) -> int:
        if t_left <= 0:
            return 0

        best_found = 0
        if not (mask[curr] & opened):
            released_pressure = (t_left - 1) * valves[curr].flow
            opened |= mask[curr]
            opening_delay = 1 if (released_pressure > 0) else 0

            for adj, time_to_reach in valves[curr].tunnels.items():
                # Only move to another valve after opening current valve =>
                # There is no need to move to another valve without
                # opening current valve, because the Floyd-Warshall
                # algorithm enforces it implicitly
                best_found = max(
                    best_found,
                    released_pressure
                    + search(
                        adj, opened, t_left - time_to_reach - opening_delay, in_parallel
                    ),
                )

            if in_parallel:
                # Suppose a second agent starting the search knowing that, by this point,
                # the first agent would have opened already the some valves.
                # In this case, it would need only to look for the remaining valves with
                # the full time
                best_found = max(
                    best_found, search(start, opened ^ mask[start], total_time, False)
                )

        return best_found

    return search(start, 0, total_time, with_help)


@Timer.timeit
def parse(filename: os.PathLike) -> List[str]:
    with open(filename, "r") as file:
        report = file.read().strip().split("\n")
    return report


@Timer.timeit
def solve(filename: os.PathLike) -> Tuple[int, int]:
    report = parse(filename)
    valves = build_graph(report)
    part1 = maximize_released_pressure(valves, 30, False)
    part2 = maximize_released_pressure(valves, 26, True)

    return part1, part2
