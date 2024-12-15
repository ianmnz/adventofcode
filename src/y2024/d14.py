# Advent of Code : Day 14 - Restroom Redoubt
# https://adventofcode.com/2024/day/14

import re
from statistics import variance
from typing import NamedTuple

from helpers import Timer, load_input_data

WIDTH = 101  # x
HEIGHT = 103  # y


class Vec2D(NamedTuple):
    x: int
    y: int


class Robot(NamedTuple):
    P: Vec2D
    V: Vec2D


def simulate_robot_position(robot: Robot, nb_steps: int) -> Vec2D:
    x = (robot.P.x + robot.V.x * nb_steps) % WIDTH
    y = (robot.P.y + robot.V.y * nb_steps) % HEIGHT
    return Vec2D(x, y)


@Timer.timeit
def compute_safety_factor(robots: list[Robot], nb_steps: int) -> int:
    Q = [-1, 0, 0, 0, 0]

    MIDDLE_W = WIDTH // 2
    MIDDLE_H = HEIGHT // 2

    for robot in robots:
        P = simulate_robot_position(robot, nb_steps)

        if P.x < MIDDLE_W:
            if P.y < MIDDLE_H:  # Top-left
                Q[2] += 1
            elif P.y > MIDDLE_H:  # Bottom-left
                Q[3] += 1

        elif P.x > MIDDLE_W:
            if P.y < MIDDLE_H:  # Top-right
                Q[1] += 1
            elif P.y > MIDDLE_H:  # Bottom-right
                Q[4] += 1

    return Q[1] * Q[2] * Q[3] * Q[4]


@Timer.timeit
def find_easter_egg(robots: list[Robot]) -> int:
    # Based on:
    # https://www.reddit.com/r/adventofcode/comments/1hdvhvu/comment/m1zws1g/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
    bx, bxvar = 0, float("inf")
    by, byvar = 0, float("inf")

    # Strong hypothesis:
    # The configuration with least variance is the one with the Christmas tree
    for n in range(max(WIDTH, HEIGHT)):
        xs, ys = zip(*(simulate_robot_position(robot, n) for robot in robots))

        if (xvar := variance(xs)) < bxvar:
            bx, bxvar = n, xvar

        if (yvar := variance(ys)) < byvar:
            by, byvar = n, yvar

    return bx + ((pow(WIDTH, -1, HEIGHT) * (by - bx)) % HEIGHT) * WIDTH


def draw(robots: list[Robot], nb_steps: int) -> None:
    grid = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]

    for robot in robots:
        P = simulate_robot_position(robot, nb_steps)
        grid[P.y][P.x] = "█"

    for row in grid:
        print("".join(row))
    print()


@Timer.timeit
def parse(data: str) -> list[Robot]:
    return [
        Robot(Vec2D(int(px), int(py)), Vec2D(int(vx), int(vy)))
        for px, py, vx, vy in re.findall(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)", data)
    ]


@Timer.timeit
def solve(data: str) -> tuple[int, int]:
    robots = parse(data)
    part1 = compute_safety_factor(robots, 100)
    part2 = find_easter_egg(robots)

    # draw(robots, part2)

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2024, 14)))
