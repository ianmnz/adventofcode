# Advent of Code : Day 22 - Monkey Map
# https://adventofcode.com/2022/day/22

import math
import os
import re
from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple

from helpers import Timer

UP = -1 + 0j
DOWN = 1 + 0j
RIGHT = 0 + 1j
LEFT = 0 - 1j

DIRECTIONS = [RIGHT, DOWN, LEFT, UP]
NB_DIR = len(DIRECTIONS)

# Using strategy proposed by smrq here:
# https://www.reddit.com/r/adventofcode/comments/zsct8w/comment/j184mn7/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
# List of adjacent faces of a face in clockwise direction
CLOCKWISE_CUBE_FACES = {
    "F": ["T", "R", "D", "L"],  # Front
    "R": ["T", "B", "D", "F"],  # Right
    "T": ["R", "F", "L", "B"],  # Top
}
CLOCKWISE_CUBE_FACES["B"] = list(reversed(CLOCKWISE_CUBE_FACES["F"]))  # Back
CLOCKWISE_CUBE_FACES["L"] = list(reversed(CLOCKWISE_CUBE_FACES["R"]))  # Left
CLOCKWISE_CUBE_FACES["D"] = list(reversed(CLOCKWISE_CUBE_FACES["T"]))  # Down


@dataclass
class Face:
    pos: complex
    heading: str = field(init=False, default="")
    edges: Dict[complex, str] = field(init=False, default_factory=dict)

    def fold(self, heading: str, _from: complex, edge: str) -> None:
        self.heading = heading

        idx = DIRECTIONS.index(_from)
        f_idx = CLOCKWISE_CUBE_FACES[heading].index(edge)

        for i in range(NB_DIR):
            dz = DIRECTIONS[(idx + i) % NB_DIR]
            face = CLOCKWISE_CUBE_FACES[heading][(f_idx + i) % NB_DIR]
            self.edges[dz] = face


@dataclass
class Wrapper:
    walls: Set[complex]
    wrap: Dict[Tuple[complex, complex], Tuple[complex, complex]]


@dataclass
class Turtle:
    pos: complex
    dir: complex = field(init=False, default=RIGHT)

    def move(self, length: str, wrapper: Wrapper) -> None:
        for _ in range(int(length)):
            if (self.dir, self.pos) in wrapper.wrap:
                dir, pos = wrapper.wrap[(self.dir, self.pos)]
            else:
                pos = self.pos + self.dir
                dir = self.dir

            if pos in wrapper.walls:
                break

            self.pos = pos
            self.dir = dir

    def turn(self, direction: str) -> None:
        if direction == "L":
            self.dir *= 1j
        elif direction == "R":
            self.dir *= -1j


def is_pos_valid(board: List[List[str]], z: complex, dz: complex) -> bool:
    pos = z + dz
    x, y = int(pos.real), int(pos.imag)
    try:
        if board[x][y] == " ":
            return False
        if x < 0 or y < 0:
            return False
        return True

    except IndexError:
        return False


@Timer.timeit
def fold(faces: Dict[complex, Face]) -> Dict[str, Face]:
    # Arbitrarily choose the first as Top
    # and the face right to it as Right
    first = next(iter(faces))
    faces[first].fold("T", RIGHT, "R")

    face_per_headings = {"T": faces[first]}

    queue = [faces[first]]
    while queue:
        face = queue.pop()

        z = face.pos

        if (north := faces.get(z + UP)) is not None and (not north.heading):
            north.fold(face.edges[UP], DOWN, face.heading)
            queue.append(north)

            face_per_headings[face.edges[UP]] = north

        if (south := faces.get(z + DOWN)) is not None and (not south.heading):
            south.fold(face.edges[DOWN], UP, face.heading)
            queue.append(south)

            face_per_headings[face.edges[DOWN]] = south

        if (east := faces.get(z + RIGHT)) is not None and (not east.heading):
            east.fold(face.edges[RIGHT], LEFT, face.heading)
            queue.append(east)

            face_per_headings[face.edges[RIGHT]] = east

        if (west := faces.get(z + LEFT)) is not None and (not west.heading):
            west.fold(face.edges[LEFT], RIGHT, face.heading)
            queue.append(west)

            face_per_headings[face.edges[LEFT]] = west

    return face_per_headings


def find_start(board: List[List[str]]) -> complex:
    for i, row in enumerate(board):
        for j, col in enumerate(row):
            if col != " ":
                return complex(i, j)
    return -1


@Timer.timeit
def build_wrappers(board: List[List[str]]) -> Tuple[Wrapper, Wrapper]:
    walls = set()
    torus = {}
    cube = {}
    region_length = int(math.sqrt(sum(col != " " for row in board for col in row) / 6))

    # Auxiliary dicts
    # for torus
    boundaries = {UP: {}, DOWN: {}, LEFT: {}, RIGHT: {}}

    # for cube
    faces = {}
    face_boundaries = {}

    for i, row in enumerate(board):
        q_i, r_i = divmod(i, region_length)

        for j, col in enumerate(row):
            if col == " ":
                continue

            z = complex(i, j)

            q_j, r_j = divmod(j, region_length)
            q = complex(q_i, q_j)
            r = complex(r_i, r_j)

            if r == 0:
                # Found a new cube face
                faces[q] = Face(q)
                face_boundaries[q] = {
                    RIGHT: [],
                    DOWN: [],
                    LEFT: [],
                    UP: [],
                }

            if col == "#":
                walls.add(z)

            if not is_pos_valid(board, z, UP):
                boundaries[UP][j] = i
                face_boundaries[q][UP].append(r)

            if not is_pos_valid(board, z, DOWN):
                boundaries[DOWN][j] = i
                face_boundaries[q][DOWN].append(r)

            if not is_pos_valid(board, z, LEFT):
                boundaries[LEFT][i] = j
                face_boundaries[q][LEFT].append(r)

            if not is_pos_valid(board, z, RIGHT):
                boundaries[RIGHT][i] = j
                face_boundaries[q][RIGHT].append(r)

    # Build torus wrapper ---
    for col, top_row in boundaries[UP].items():
        bottom_row = boundaries[DOWN][col]
        top = complex(top_row, col)
        bottom = complex(bottom_row, col)

        torus[(UP, top)] = (UP, bottom)
        torus[(DOWN, bottom)] = (DOWN, top)

    for row, right_col in boundaries[RIGHT].items():
        left_col = boundaries[LEFT][row]
        left = complex(row, left_col)
        right = complex(row, right_col)

        torus[(RIGHT, right)] = (RIGHT, left)
        torus[(LEFT, left)] = (LEFT, right)
    # ---

    # Build cube wrapper ---
    face_per_headings = fold(faces)

    for face_pos, directions in face_boundaries.items():
        face = faces[face_pos]
        board_pos = region_length * face_pos

        for dz, boundary in directions.items():
            heading = face.edges[dz]
            adj_face = face_per_headings[heading]
            board_adj_pos = region_length * adj_face.pos

            idx = DIRECTIONS.index(dz)

            for r in boundary:
                rdz = r + dz
                rdz_x, rdz_y = rdz.real % region_length, rdz.imag % region_length

                for i in range(NB_DIR):
                    if (
                        adj_face.edges[DIRECTIONS[(idx + i + 2) % NB_DIR]]
                        == face.heading
                    ):
                        break

                    # 90-degrees clockwise rotation
                    rdz_x, rdz_y = (rdz_y, (region_length - 1) - rdz_x)

                cube[(dz, board_pos + r)] = (
                    DIRECTIONS[(idx + i) % NB_DIR],
                    board_adj_pos + complex(rdz_x, rdz_y),
                )
    # ---

    return Wrapper(walls, torus), Wrapper(walls, cube)


@Timer.timeit
def get_final_password(
    start: complex, wrapper: Wrapper, instructions: List[str]
) -> int:
    turtle = Turtle(start)

    for instruction in instructions:
        if instruction.isnumeric():
            turtle.move(instruction, wrapper)
        else:
            turtle.turn(instruction)

    return int(
        1000 * (turtle.pos.real + 1)
        + 4 * (turtle.pos.imag + 1)
        + DIRECTIONS.index(turtle.dir)
    )


@Timer.timeit
def parse(filename: os.PathLike) -> Tuple[List[List[str]], List[str]]:
    with open(filename, "r") as file:
        lines, path = file.read().rstrip().split("\n\n")

    board = [[col for col in row] for row in lines.split("\n")]
    instructions = [move for move in re.findall(r"\d+|[RL]", path)]

    return board, instructions


@Timer.timeit
def solve(filename: os.PathLike) -> Tuple[int, int]:
    board, instructions = parse(filename)
    start = find_start(board)
    torus, cube = build_wrappers(board)
    part1 = get_final_password(start, torus, instructions)
    part2 = get_final_password(start, cube, instructions)

    return part1, part2


def main() -> None:
    from pathlib import Path

    res = solve(Path(__file__).parent / "input.txt")

    assert res[0] == 123_046, f"Part1 = {res[0]}"
    assert res[1] == 195_032, f"Part2 = {res[1]}"


if __name__ == "__main__":
    main()
