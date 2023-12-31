# Advent of Code : Day 10 - Pipe Maze
# https://adventofcode.com/2023/day/10


from typing import Dict, List, Set


N, S, E, W = -1, +1, +1j, -1j
connections = {
    '|': [N, S],
    '-': [W, E],
    'L': [N, E],
    'J': [N, W],
    'F': [S, E],
    '7': [S, W],
    '.': []
}


def follow_pipes(maze: List[str]) -> Set[complex]:
    n = len(maze)
    m = len(maze[0])

    def is_valid(z: complex) -> bool:
        return ((0 <= z.real < n) and (0 <= z.imag < m))

    def find_start() -> complex:
        for i in range(n):
            for j in range(m):
                if maze[i][j] == 'S':
                    start = complex(i, j)
                    matches = set()
                    for dr, pipes in zip((N, S, W, E), ('F|7', 'L|J', 'L-F', '7-J')):
                        char = start + dr

                        if is_valid(char) and maze[int(char.real)][int(char.imag)] in pipes:
                            matches.add(dr)

                    if   matches == {N, S}: maze[i] = maze[i].replace('S', '|')
                    elif matches == {N, E}: maze[i] = maze[i].replace('S', 'L')
                    elif matches == {N, W}: maze[i] = maze[i].replace('S', 'J')
                    elif matches == {S, E}: maze[i] = maze[i].replace('S', 'F')
                    elif matches == {S, W}: maze[i] = maze[i].replace('S', '7')
                    else: maze[i] = maze[i].replace('S', '-')  # matches == {E, W}

                    return start

    start = find_start()

    graph: Dict[complex, List[complex]] = dict()
    for i in range(n):
        for j in range(m):
            pos = complex(i, j)
            char = maze[i][j]
            graph[pos] = [pos + connection for connection in connections[char] if is_valid(pos + connection)]

    visited = {start}
    while queue := graph[start]:
        curr = queue.pop(0)
        visited.add(curr)
        queue.extend([pos for pos in graph[curr] if pos not in visited])

    return visited


def find_farthest_position(maze: List[str]) -> int:
    return len(follow_pipes(maze))//2


def find_enclosed_area(maze: List[str]) -> int:
    enclosed_area = 0
    visited = follow_pipes(maze)

    for i, row in enumerate(maze):
        is_inside = False
        for j, col in enumerate(row):
            if complex(i, j) not in visited:
                enclosed_area += is_inside
            else:
                is_inside ^= (col in 'F|7')

    return enclosed_area


def main():
    import os
    import sys

    # To be able to import the helpers module
    sys.path.append(os.path.dirname(                                        # Project
                        os.path.dirname(                                    # Year
                            os.path.dirname(os.path.abspath(__file__)))))   # Day

    from helpers import Timer

    with open("input.txt", "r") as file:
        maze = file.read().splitlines()
        maze_cp = maze.copy()

    # --- Part 1 --- #
    with Timer():
        print("Nb of steps to farthest position from starting point:", find_farthest_position(maze))  # 6725

    # --- Part 2 --- #
    with Timer():
        print("Nb of tiles enclosed by the loop:", find_enclosed_area(maze_cp))  # 383


if __name__ == "__main__":
    main()
