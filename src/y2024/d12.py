# Advent of Code : Day 12 - Garden Groups
# https://adventofcode.com/2024/day/12

from collections import deque

from helpers import Timer, load_input_data

DIRS = [-1 + 0j, 1j, 1 + 0j, -1j]  # N, E, S, W


def flood_fill(
    start: complex, garden: dict[complex, str], index: str
) -> tuple[int, int, int]:
    plot = garden[start]
    area = 0
    perimeter = 0
    corners = 0

    def is_adjacent(z: complex) -> bool:
        return (z in garden) and garden[z] in (plot, index)

    def count_corners(z: complex, adjacency: list[bool]) -> int:
        corners = 0

        is_top_adj = adjacency[0]
        is_right_adj = adjacency[1]
        is_down_adj = adjacency[2]
        is_left_adj = adjacency[3]

        # Outer
        corners += not is_top_adj and not is_left_adj
        corners += not is_down_adj and not is_left_adj
        corners += not is_top_adj and not is_right_adj
        corners += not is_down_adj and not is_right_adj

        # Inner
        corners += is_top_adj and is_left_adj and not is_adjacent(z + DIRS[0] + DIRS[3])
        corners += (
            is_down_adj and is_left_adj and not is_adjacent(z + DIRS[2] + DIRS[3])
        )
        corners += (
            is_top_adj and is_right_adj and not is_adjacent(z + DIRS[0] + DIRS[1])
        )
        corners += (
            is_down_adj and is_right_adj and not is_adjacent(z + DIRS[2] + DIRS[1])
        )

        return corners

    queue = deque([start])
    while queue:
        curr = queue.popleft()

        if garden[curr] == index:
            continue

        garden[curr] = index
        area += 1
        perimeter += 4
        adjacency = [False for _ in range(len(DIRS))]

        for i, dir in enumerate(DIRS):
            if is_adjacent(adj := curr + dir):
                queue.append(adj)
                perimeter -= 1
                adjacency[i] = True

        corners += count_corners(curr, adjacency)

    return area, perimeter, corners


@Timer.timeit
def compute_fencing_price(garden: dict[complex, str]) -> tuple[int, int]:
    price1 = 0
    price2 = 0
    regions: set[str] = set()

    for pos in garden:
        if garden[pos] not in regions:
            index = str(len(regions))
            regions.add(index)

            area, perimeter, corners = flood_fill(pos, garden, index)

            price1 += area * perimeter

            # Counting sides of a polygon is equivalent to count
            # the number of corners of such polygon
            price2 += area * corners

    return price1, price2


@Timer.timeit
def parse(data: str) -> dict[complex, str]:
    return {
        complex(i, j): col
        for i, row in enumerate(data.splitlines())
        for j, col in enumerate(row)
    }


@Timer.timeit
def solve(data: str) -> tuple[int, int]:
    garden = parse(data)
    part1, part2 = compute_fencing_price(garden)

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2024, 12)))
