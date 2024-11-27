# Advent of Code : Day 19 - Not Enough Minerals
# https://adventofcode.com/2022/day/19

import os
import re
from dataclasses import dataclass
from typing import Dict, List, Tuple, TypedDict

from ortools.linear_solver import pywraplp

from helpers import Timer


class Resource(TypedDict):
    ore: int
    clay: int
    obsidian: int
    geode: int


@dataclass
class Blueprint:
    id: int
    cost: Dict[str, Resource]


def mip_solve(costs: Dict[str, Resource], T: int) -> int:
    solver = pywraplp.Solver.CreateSolver("SAT")

    # Variables
    Ro = []  # Nb of ore robots for each instant t
    Rc = []  # Nb of clay robots for each instant t
    Rb = []  # Nb of obsidian robots for each instant t
    Rg = []  # Nb of geode robots for each instant t

    Ro.append(solver.IntVar(1, 1, "Ro_0"))
    Rc.append(solver.IntVar(0, 0, "Rc_0"))
    Rb.append(solver.IntVar(0, 0, "Rb_0"))
    Rg.append(solver.IntVar(0, 0, "Rg_0"))

    for t in range(1, T):
        Ro.append(solver.IntVar(0, T, f"Ro_{t}"))
        Rc.append(solver.IntVar(0, T, f"Rc_{t}"))
        Rb.append(solver.IntVar(0, T, f"Rb_{t}"))
        Rg.append(solver.IntVar(0, T, f"Rg_{t}"))

    # Constraints
    accum_ore_in_t_2 = 0  # Total produced ore up to t-2
    accum_cla_in_t_2 = 0  # Total produced clay up to t-2
    accum_obs_in_t_2 = 0  # Total produced obsidian up to t-2

    for t in range(1, T):
        # Max build 1 robot per timestep
        solver.Add(
            Ro[t] + Rc[t] + Rb[t] + Rg[t]
            <= 1 + Ro[t - 1] + Rc[t - 1] + Rb[t - 1] + Rg[t - 1],
            f"Factory_in_t{t}",
        )

        # No robots losses
        solver.Add(Ro[t - 1] <= Ro[t], f"No_Ro_loss_in_t{t}")
        solver.Add(Rc[t - 1] <= Rc[t], f"No_Rc_loss_in_t{t}")
        solver.Add(Rb[t - 1] <= Rb[t], f"No_Rb_loss_in_t{t}")
        solver.Add(Rg[t - 1] <= Rg[t], f"No_Rg_loss_in_t{t}")

        # Building cost
        if t >= 2:
            accum_ore_in_t_2 += Ro[t - 2]
            accum_cla_in_t_2 += Rc[t - 2]
            accum_obs_in_t_2 += Rb[t - 2]

        # costs[X][Y] Cost in Y resource for X robot
        # Ore robot
        solver.Add(
            costs["ore"]["ore"] * (Ro[t] - 1)
            + costs["clay"]["ore"] * Rc[t - 1]
            + costs["obsidian"]["ore"] * Rb[t - 1]
            + costs["geode"]["ore"] * Rg[t - 1]
            <= accum_ore_in_t_2,
            f"Ore_robot_ore_cost_in_t{t}",
        )

        # Clay robot
        solver.Add(
            costs["ore"]["ore"] * (Ro[t - 1] - 1)
            + costs["clay"]["ore"] * Rc[t]
            + costs["obsidian"]["ore"] * Rb[t - 1]
            + costs["geode"]["ore"] * Rg[t - 1]
            <= accum_ore_in_t_2,
            f"Clay_robot_ore_cost_in_t{t}",
        )

        # Obsidian robot
        solver.Add(
            costs["ore"]["ore"] * (Ro[t - 1] - 1)
            + costs["clay"]["ore"] * Rc[t - 1]
            + costs["obsidian"]["ore"] * Rb[t]
            + costs["geode"]["ore"] * Rg[t - 1]
            <= accum_ore_in_t_2,
            f"Obsidian_robot_ore_cost_in_t{t}",
        )
        solver.Add(
            costs["obsidian"]["clay"] * Rb[t] <= accum_cla_in_t_2,
            f"Obsidian_robot_clay_cost_in_t{t}",
        )

        # Geode robot
        solver.Add(
            costs["ore"]["ore"] * (Ro[t - 1] - 1)
            + costs["clay"]["ore"] * Rc[t - 1]
            + costs["obsidian"]["ore"] * Rb[t - 1]
            + costs["geode"]["ore"] * Rg[t]
            <= accum_ore_in_t_2,
            f"Geode_robot_ore_cost_in_t{t}",
        )
        solver.Add(
            costs["geode"]["obsidian"] * Rg[t] <= accum_obs_in_t_2,
            f"Geode_robot_obsidian_cost_in_t{t}",
        )

    # Objective
    solver.Maximize(sum([Rg_t for Rg_t in Rg]))

    solver.Solve()

    return solver.Objective().Value()


@Timer.timeit
def get_sum_of_quality_level(blueprints: List[Blueprint], T: int) -> int:
    quality_level = 0
    for blueprint in blueprints:
        nb_open_geodes = mip_solve(blueprint.cost, T)
        quality_level += blueprint.id * nb_open_geodes

    return int(quality_level)


@Timer.timeit
def get_product_of_nb_opened(blueprints: List[Blueprint], T: int, n: int) -> int:
    prod = 1
    for blueprint in blueprints[:n]:
        nb_open_geodes = mip_solve(blueprint.cost, T)
        prod *= nb_open_geodes

    return int(prod)


@Timer.timeit
def parse(filename: os.PathLike) -> List[Blueprint]:
    with open(filename, "r") as file:
        lines = file.read().strip().split("\n")

    blueprints = []
    pattern = re.compile(
        r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian."
    )
    for line in lines:
        match = pattern.match(line)
        if match is not None:
            cost = {}
            cost["ore"] = Resource(ore=int(match.group(2)), clay=0, obsidian=0, geode=0)
            cost["clay"] = Resource(
                ore=int(match.group(3)), clay=0, obsidian=0, geode=0
            )
            cost["obsidian"] = Resource(
                ore=int(match.group(4)), clay=int(match.group(5)), obsidian=0, geode=0
            )
            cost["geode"] = Resource(
                ore=int(match.group(6)), clay=0, obsidian=int(match.group(7)), geode=0
            )

            blueprints.append(Blueprint(int(match.group(1)), cost))

    return blueprints


@Timer.timeit
def solve(filename: os.PathLike) -> Tuple[int, int]:
    blueprints = parse(filename)
    part1 = get_sum_of_quality_level(blueprints, 24)
    part2 = get_product_of_nb_opened(blueprints, 32, 3)

    return part1, part2
