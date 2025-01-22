# Advent of Code : Day 17 - Clumsy Crucible
# https://adventofcode.com/2023/day/17

from heapq import heappop, heappush

from helpers import Timer, load_input_data


@Timer.timeit
def build_graph(heatmap: list[list[int]]) -> dict[tuple[int], int]:
    return {(i, j): col for i, row in enumerate(heatmap) for j, col in enumerate(row)}


@Timer.timeit
def find_shortest_path(graph: dict[tuple[int], int], lower: int, upper: int) -> int:
    source = (0, 0)
    dest = [*graph][-1]

    heap = [(0, *source, 1, 0), (0, *source, 0, 1)]
    visited = set()

    while heap:
        cost, px, py, dx, dy = heappop(heap)

        if (px, py) == dest:
            return cost

        if (px, py, dx, dy) in visited:
            continue

        visited.add((px, py, dx, dy))

        for rx, ry in [(dy, -dx), (-dy, dx)]:  # rotate -pi/2, +pi/2
            x, y, c = px, py, cost
            for step in range(1, upper + 1):
                x += rx
                y += ry

                if (x, y) in graph:
                    c += graph[(x, y)]
                    if step >= lower:
                        heappush(heap, (c, x, y, rx, ry))
                else:
                    break
    return -1


@Timer.timeit
def parse(data: str) -> list[list[int]]:
    heatmap = [[int(heatloss) for heatloss in line] for line in data.split("\n")]
    return heatmap


@Timer.timeit
def solve(data: str) -> tuple[int, int]:
    heatmap = parse(data)
    graph = build_graph(heatmap)
    part1 = find_shortest_path(graph, 1, 3)
    part2 = find_shortest_path(graph, 4, 10)

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2023, 17)))
