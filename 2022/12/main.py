# Advent of Code : Day 12 - Hill Climbing Algorithm
# https://adventofcode.com/2022/day/12


import numpy as np
from typing import Tuple, Optional, Dict, Set


class Node:
    def __init__(self, pos: Tuple[int, int], target: Tuple[int, int], parent: Optional['Node'] = None) -> None:
        self.pos: Tuple[int, int] = pos
        self.parent: Optional['Node'] = parent

        self.g: int = 0
        if parent is not None:
            self.g = parent.g + 1

        # Manhattan distance
        self.h: int = abs(target[0] - self.pos[0]) + abs(target[1] - self.pos[1])

        self.f: int = self.g + self.h


def current(openlist: Dict[Tuple[int, int], Node]) -> Node:
    curr = openlist[next(iter(openlist))]
    for node in openlist.values():
        if node.f < curr.f:
            curr = node
    return curr


def successors(node: Node, target: Tuple[int, int], graph: np.array) -> Set[Node]:
    x, y = node.pos
    corr_x, corr_y = x + 1, y + 1 # Padding correction
    height = graph[corr_x][corr_y]

    successorslist = set()

    if graph[corr_x + 1][corr_y] <= height + 1:
        rsuccessor = Node((x + 1, y), target, node)
        successorslist.add(rsuccessor)

    if graph[corr_x - 1][corr_y] <= height + 1:
        lsuccessor = Node((x - 1, y), target, node)
        successorslist.add(lsuccessor)

    if graph[corr_x][corr_y + 1] <= height + 1:
        usuccessor = Node((x, y + 1), target, node)
        successorslist.add(usuccessor)

    if graph[corr_x][corr_y - 1] <= height + 1:
        dsuccessor = Node((x, y - 1), target, node)
        successorslist.add(dsuccessor)

    return successorslist


def search(start: Tuple[int, int], target: Tuple[int, int], heightmap: np.array) -> Set[Node]:
    openlist: Dict[Tuple[int, int], Node] = dict()
    closedlist: Dict[Tuple[int, int],Node] = dict()
    path_tails: Set[Node] = set()

    # Search
    openlist[start] = Node(start, target)

    while openlist:
        curr = current(openlist)

        del openlist[curr.pos]

        successorslist = successors(curr, target, heightmap)

        for successor in successorslist:
            if successor.h == 0:
                path_tails.add(successor)
                continue

            if (successor.pos in openlist) and (openlist[successor.pos].f < successor.f):
                continue

            if (successor.pos in closedlist) and (closedlist[successor.pos].f < successor.f):
                continue

            openlist[successor.pos] = successor

        closedlist[curr.pos] = curr

    return path_tails


def char_to_int(item: str) -> int:
    d = {
        'a' :  1,
        'b' :  2,
        'c' :  3,
        'd' :  4,
        'e' :  5,
        'f' :  6,
        'g' :  7,
        'h' :  8,
        'i' :  9,
        'j' : 10,
        'k' : 11,
        'l' : 12,
        'm' : 13,
        'n' : 14,
        'o' : 15,
        'p' : 16,
        'q' : 17,
        'r' : 18,
        's' : 19,
        't' : 20,
        'u' : 21,
        'v' : 22,
        'w' : 23,
        'x' : 24,
        'y' : 25,
        'z' : 26
    }
    return d[item]

def main():
    heightmap = []
    starts = []

    with open('input.txt', 'r') as file:
        found_start = False
        found_target = False
        for i, line in enumerate(file):
            row = list(line.strip())

            if (not found_start) and ('S' in row):
                found_start = True
                j = row.index('S')
                start_S = (i, j)
                row[j] = 'a'

            if (not found_target) and ('E' in row):
                found_target = True
                j = row.index('E')
                target = (i, j)
                row[j] = 'z'

            for j, char in enumerate(row):
                if char == 'a':
                    starts.append((i, j))

            heightmap.append(list(map(char_to_int, row)))

    heightmap = np.pad(np.array(heightmap), 1, 'constant', constant_values=1000)

    path_tails = search(start_S, target, heightmap)
    min_path_length = 10000

    for node in path_tails:
        path_length = 0
        while node.parent is not None:
            path_length += 1
            node = node.parent

        if path_length < min_path_length:
            min_path_length = path_length

    # Answer part 1 :
    print(f"Number of steps on the smallest path: {min_path_length}") # 517

    min_path_length = 10000
    min_path_start = (0, 0)
    for start in starts:
        path_tails = search(start, target, heightmap)

        for node in path_tails:
            path_length = 0
            while node.parent is not None:
                path_length += 1
                node = node.parent

            if path_length < min_path_length:
                min_path_length = path_length
                min_path_start = start

    # Answer part 2 :
    print(f"Number of steps on the smallest path starting from {min_path_start}: {min_path_length}") # (13, 0) - 512

if __name__ == "__main__":
    main()