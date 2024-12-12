# Advent of Code : Day 12 - Garden Groups
# https://adventofcode.com/2024/day/12

from collections import deque

from helpers import Timer, load_input_data

N = -1 + 0j
E = 0 + 1j
S = 1 + 0j
W = 0 - 1j


def flood_fill(
    start: complex, garden: dict[complex, str], index: str
) -> tuple[int, int, int]:
    plot = garden[start]
    area = 0
    perimeter = 0
    corners = 0

    def is_adj(z: complex) -> bool:
        return (z in garden) and garden[z] in (plot, index)

    def count_corners(z: complex) -> int:
        corners = 0

        is_top_adj = is_adj(z + N)
        is_right_adj = is_adj(z + E)
        is_down_adj = is_adj(z + S)
        is_left_adj = is_adj(z + W)

        # Outer
        corners += not is_top_adj and not is_left_adj
        corners += not is_down_adj and not is_left_adj
        corners += not is_top_adj and not is_right_adj
        corners += not is_down_adj and not is_right_adj

        # Inner
        corners += is_top_adj and is_left_adj and not is_adj(z + N + W)
        corners += is_down_adj and is_left_adj and not is_adj(z + S + W)
        corners += is_top_adj and is_right_adj and not is_adj(z + N + E)
        corners += is_down_adj and is_right_adj and not is_adj(z + S + E)

        return corners

    queue = deque([start])
    while queue:
        curr = queue.popleft()

        if garden[curr] == index:
            continue

        garden[curr] = index
        area += 1
        perimeter += 4

        if is_adj(top := curr + N):
            queue.append(top)
            perimeter -= 1

        if is_adj(right := curr + E):
            queue.append(right)
            perimeter -= 1

        if is_adj(down := curr + S):
            queue.append(down)
            perimeter -= 1

        if is_adj(left := curr + W):
            queue.append(left)
            perimeter -= 1

        corners += count_corners(curr)

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
