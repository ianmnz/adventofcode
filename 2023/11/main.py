# Advent of Code : Day 11 - Cosmic Expansion
# https://adventofcode.com/2023/day/11


from typing import List


def compute_distances_matrix(image: List[str], expansion: int) -> List[List[int]]:
    empty_rows = set(range(len(image)))
    empty_cols = set(range(len(image[0])))

    galaxies = []

    for i, row in enumerate(image):
        for j, col in enumerate(row):
            if col == '#':
                empty_rows.discard(i)
                empty_cols.discard(j)
                galaxies.append((i, j))

    n = len(galaxies)
    distances = [[0 for _ in range(n)] for _ in range(n)]

    for a in range(n):
        galaxy_a = galaxies[a]
        for b in range(a + 1, n):
            galaxy_b = galaxies[b]

            low_i, upp_i = sorted((galaxy_a[0], galaxy_b[0]))
            dist_i = (upp_i - low_i) + sum([expansion - 1 if low_i < row < upp_i else 0 for row in empty_rows])

            low_j, upp_j = sorted((galaxy_a[1], galaxy_b[1]))
            dist_j = (upp_j - low_j) + sum([expansion - 1 if low_j < col < upp_j else 0 for col in empty_cols])

            distances[a][b] = distances[b][a] = int(dist_i + dist_j)    # manhattan distance

    return distances


def calculate_sum_of_distances(image: List[str], expansion: int) -> int:
    distances = compute_distances_matrix(image, expansion)
    return sum(map(sum, distances)) // 2


def main():
    import os
    import sys

    # To be able to import the helpers module
    sys.path.append(os.path.dirname(                                        # Project
                        os.path.dirname(                                    # Year
                            os.path.dirname(os.path.abspath(__file__)))))   # Day

    from helpers import Timer

    with open("input.txt", "r") as file:
        image = file.read().split('\n')

    # --- Part 1 --- #
    with Timer():
        print("Sum of distances:", calculate_sum_of_distances(image, 2))  # 9445168

    # --- Part 2 --- #
    with Timer():
        print("Sum of distances for older universe:", calculate_sum_of_distances(image, 1_000_000))  # 742305960572


if __name__ == "__main__":
    main()
