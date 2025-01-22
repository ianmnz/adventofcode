# Advent of Code : Day 24 - Never Tell Me The Odds
# https://adventofcode.com/2023/day/24

import collections
import itertools

from helpers import Timer, load_input_data

Vector3d = collections.namedtuple("Vector3d", ["x", "y", "z"])


@Timer.timeit
def get_vectors(hailstorm: list[list[str]]) -> list[tuple[Vector3d]]:
    vectors = []
    for hailstone in hailstorm:
        pos = Vector3d(*eval(hailstone[0]))
        vel = Vector3d(*eval(hailstone[1]))
        vectors.append((pos, vel))

    return vectors


@Timer.timeit
def count_intersections(
    vectors: list[tuple[Vector3d]], lower_bound: int, upper_bound: int
) -> int:
    count = 0
    for (P1, V1), (P2, V2) in itertools.combinations(vectors, 2):
        det = V1.x * V2.y - V1.y * V2.x

        if abs(det) < 0.001:
            # Det = 0 => No intersections whatsoever
            # To avoid numerical problems, we allow a small tolerance
            continue

        dP = Vector3d(P1.x - P2.x, P1.y - P2.y, P1.z - P2.z)

        # P1 + t * V1
        t = 1 / det * (-V2.y * dP.x + V2.x * dP.y)

        # P2 + s * V2
        s = 1 / det * (-V1.y * dP.x + V1.x * dP.y)

        if t < 0 or s < 0:
            continue

        X = P1.x + t * V1.x
        Y = P1.y + t * V1.y

        if (lower_bound <= X <= upper_bound) and (lower_bound <= Y <= upper_bound):
            count += 1

    return count


@Timer.timeit
def find_rock_launch_vector(vectors: list[tuple[Vector3d]]) -> int:
    import sympy

    Px = sympy.Symbol("Px")
    Py = sympy.Symbol("Py")
    Pz = sympy.Symbol("Pz")

    Vx = sympy.Symbol("Vx")
    Vy = sympy.Symbol("Vy")
    Vz = sympy.Symbol("Vz")

    variables = [Px, Py, Pz, Vx, Vy, Vz]
    equations = []

    """
    We have 3 position variables Px, Py, Pz
    And 3 velocity variables Vx, Vy, Vz

    Given a time step t, for each relation
    P + t * V = Pi + t * Vi => P + t * V - Pi - t * Vi = 0
    where i is the i-th hailstone, we get 3 equations (for x, y and z)

    Adding 3 time steps t1, t2, t3, we obtain 9 equations on total
    for 9 variables (previous 6 plus the 3 time variables) and then
    our system of equations has a unique solution
    """
    for i, (Pi, Vi) in enumerate(vectors[:3], 1):
        t = sympy.Symbol(f"t{i}")

        eq_x = Px + t * Vx - Pi.x - t * Vi.x
        eq_y = Py + t * Vy - Pi.y - t * Vi.y
        eq_z = Pz + t * Vz - Pi.z - t * Vi.z

        equations.extend([eq_x, eq_y, eq_z])
        variables.append(t)

    # Using SymPy to symbolic resolve the non-linear system of equations
    Px, Py, Pz, Vx, Vy, Vz, t1, t2, t3 = sympy.solve_poly_system(equations, *variables)[
        0
    ]

    return Px + Py + Pz


@Timer.timeit
def parse(data: str) -> list[list[str]]:
    return [line.split("@") for line in data.split("\n")]


@Timer.timeit
def solve(data: str) -> tuple[int, int]:
    hailstorm = parse(data)
    vectors = get_vectors(hailstorm)
    part1 = count_intersections(vectors, 200_000_000_000_000, 400_000_000_000_000)
    # Try with numpy and Newtons-Raphson algo
    part2 = find_rock_launch_vector(vectors)

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2023, 24)))
