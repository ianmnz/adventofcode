# Advent of Code : Day 24 - Never Tell Me The Odds
# https://adventofcode.com/2023/day/24

import collections
import itertools
import sympy
from typing import List, Tuple


Vector3d = collections.namedtuple('Vector3d', ['x', 'y', 'z'])


def get_vectors(hailstorm: List[List[str]]) -> List[Tuple[Vector3d]]:
    vectors = []
    for hailstone in hailstorm:
        pos = Vector3d(*eval(hailstone[0]))
        vel = Vector3d(*eval(hailstone[1]))
        vectors.append((pos, vel))

    return vectors


def count_intersections(vectors: List[Tuple[Vector3d]], lower_bound: int, upper_bound: int) -> int:
    count = 0
    for (P1, V1), (P2, V2) in itertools.combinations(vectors, 2):
        det = V1.x * V2.y - V1.y * V2.x

        if abs(det) < 0.001:
            # Det = 0 => No intersections whatsoever
            # To avoid numerical problems, we allow a small tolerance
            continue

        dP = Vector3d(P1.x - P2.x, P1.y - P2.y, P1.z - P2.z)

        # P1 + t * V1
        t = 1/det * (-V2.y * dP.x + V2.x * dP.y)

        # P2 + s * V2
        s = 1/det * (-V1.y * dP.x + V1.x * dP.y)

        if t < 0 or s < 0:
            continue

        X = P1.x + t * V1.x
        Y = P1.y + t * V1.y

        if (lower_bound <= X <= upper_bound) and (lower_bound <= Y <= upper_bound):
            count += 1

    return count


def find_rock_launch_vector(vectors: List[Tuple[Vector3d]]) -> Tuple[Vector3d]:
    Px = sympy.Symbol('Px')
    Py = sympy.Symbol('Py')
    Pz = sympy.Symbol('Pz')

    Vx = sympy.Symbol('Vx')
    Vy = sympy.Symbol('Vy')
    Vz = sympy.Symbol('Vz')

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
        t = sympy.Symbol(f't{i}')

        eq_x = Px + t * Vx - Pi.x - t * Vi.x
        eq_y = Py + t * Vy - Pi.y - t * Vi.y
        eq_z = Pz + t * Vz - Pi.z - t * Vi.z

        equations.extend([eq_x, eq_y, eq_z])
        variables.append(t)

    # Using SymPy to symbolic resolve the non-linear system of equations
    Px, Py, Pz, Vx, Vy, Vz, t1, t2, t3 = sympy.solve_poly_system(equations, *variables)[0]

    print(f'Position  = ({Px}, {Py}, {Pz})')
    print(f'Velocity  = ({Vx}, {Vy}, {Vz})')
    print(f'Timesteps = ({t1}, {t2}, {t3})')

    return Px + Py + Pz


def main():
    import os
    import sys

    # To be able to import the helpers module
    sys.path.append(os.path.dirname(                                        # Project
                        os.path.dirname(                                    # Year
                            os.path.dirname(os.path.abspath(__file__)))))   # Day

    from helpers import Timer

    with open("input.txt", "r") as file:
        hailstorm = [line.split('@') for line in file.read().split('\n')]

    # --- Part 1 --- #
    with Timer():
        print("Nb of future intersections inside boundaries:",
              count_intersections(get_vectors(hailstorm), 200_000_000_000_000, 400_000_000_000_000))  # 31921

    # --- Part 2 --- #
    with Timer():
        print("Sum of x, y, z coordinates of position :",
              find_rock_launch_vector(get_vectors(hailstorm)))  # 761691907059631


if __name__ == "__main__":
    main()
