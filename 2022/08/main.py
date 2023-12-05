# Advent of Code : Day 08 - Treetop Tree House
# https://adventofcode.com/2022/day/8


import numpy as np


def main() -> None:
    height_grid = []
    nb_visible_tree_from_outside_grid = 0
    max_visibility_score = 0
    max_visibility_score_tree = (0, 0)

    with open('input.txt', 'r') as file:
        for line in file:
            height_grid.append(list(line.strip()))

    height_grid = np.stack(height_grid)
    m, n = height_grid.shape

    # Left  => 1
    # Right => 2
    # Up    => 4
    # Down  => 8

    exposure_grid = np.zeros((m, n), dtype=int)
    score_grid = np.ones((m, n, 4), dtype=int)

    for i in range(m):
        max_height_left = height_grid[i, 0]
        max_height_right = height_grid[i, n-1]

        exposure_grid[i, 0] += 1 # First column
        score_grid[i, 0, 0] = 0 # First column

        exposure_grid[i, n-1] += 2 # Last column
        score_grid[i, n-1, 1] = 0 # Last column

        for j in range(1, n - 1):
            # --- Part 1 --- #
            # The highest tree up to that point
            height_left = height_grid[i, j]
            height_right = height_grid[i, n-j-1]

            if height_left > max_height_left:
                max_height_left = height_left
                exposure_grid[i, j] += 1

            if height_right > max_height_right:
                max_height_right = height_right
                exposure_grid[i, n-j-1] += 2

            # --- Part 2 --- #
            # The distance of the biggest tree
            # seeing from that direction
            score_grid[i, j, 0] = j
            score_grid[i, n-j-1, 1] = j

            found_left = False
            found_right = False
            for k in range(1, j):
                if (not found_left) and (height_grid[i, j - k] >= height_grid[i, j]):
                    score_grid[i, j, 0] = k
                    found_left = True

                if (not found_right) and (height_grid[i, n-j-1 + k] >= height_grid[i, n-j-1]):
                    score_grid[i, n-j-1, 1] = k
                    found_right = True

                if found_left and found_right:
                    break


    for j in range(n):
        max_height_up = height_grid[0, j]
        max_height_down = height_grid[m-1, j]

        exposure_grid[0, j] += 4 # First row
        score_grid[0, j, 2] = 0 # First row

        exposure_grid[m-1, j] += 8 # Last row
        score_grid[m-1, j, 3] = 0 # Last row

        for i in range(1, m - 1):
            # --- Part 1 --- #
            # The highest tree up to that point
            height_up = height_grid[i, j]
            height_down = height_grid[m-i-1, j]

            if height_up > max_height_up:
                max_height_up = height_up
                exposure_grid[i, j] += 4

            if height_down > max_height_down:
                max_height_down = height_down
                exposure_grid[m-i-1, j] += 8

            # --- Part 2 --- #
            # The distance of the biggest tree
            # seeing from that direction
            score_grid[i, j, 2] = i
            score_grid[m-i-1, j, 3] = i

            found_up = False
            found_down = False
            for k in range(1, i):
                if (not found_up) and (height_grid[i - k, j] >= height_grid[i, j]):
                    score_grid[i, j, 2] = k
                    found_up = True

                if (not found_down) and (height_grid[m-i-1 + k, j] >= height_grid[m-i-1, j]):
                    score_grid[m-i-1, j, 3] = k
                    found_down = True

                if found_up and found_down:
                    break


    # print(exposure_grid)
    nb_visible_tree_from_outside_grid = np.count_nonzero(exposure_grid)

    # Answer part 1 :
    print(f'Number of visible trees from outside the height_grid: {nb_visible_tree_from_outside_grid}') # 1805

    score_grid_reduced = np.multiply.reduce(score_grid, axis=2)
    # print(score_grid_reduced)

    max_visibility_score_tree = np.unravel_index(np.argmax(score_grid_reduced, axis=None), (m, n))
    max_visibility_score = score_grid_reduced[max_visibility_score_tree]

    # Answer part 2 :
    print(f'Highest visibility score tree: {max_visibility_score_tree}') # (77, 42)
    print(f'Highest visibility score by direction: {score_grid[max_visibility_score_tree]}') # [42 56  9 21]
    print(f'Highest visibility score: {max_visibility_score}') # 444528


if __name__ == "__main__":
    main()