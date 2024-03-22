# Advent of Code : Day 20 - Grove Positioning System
# https://adventofcode.com/2022/day/20

from typing import Dict, List, Tuple

from helpers import Timer


class Node:
    val: int
    prev: "Node"
    next: "Node"

    def __init__(self, val: int) -> None:
        self.val = val
        self.prev = self.next = self

    def __repr__(self) -> str:
        return f"Node({self.val})"


class CDLL:  # Circular Double Linked List
    n: int
    head: Node
    nodes: Dict[int, Node]

    def __init__(self, array: List[int]) -> None:
        self.n = len(array)
        self.nodes = {idx: Node(val) for idx, val in enumerate(array)}
        self.head = self.nodes[array.index(0)]

        for i in range(self.n - 1):
            self.insert(self.nodes[i], self.nodes[i + 1])

    @staticmethod
    def insert(in_list: Node, new: Node) -> None:
        # Remove new from current place
        new.prev.next = new.next
        new.next.prev = new.prev

        # Set new next to in_list
        new.next = in_list.next
        new.prev = in_list

        # Set in_list prev to new
        in_list.next.prev = new
        in_list.next = new

    def move(self, elem: int) -> None:
        n = self.n - 1
        node = self.nodes[elem]

        if node.val > 0:
            self._rotate_right(node, node.val % n)
        elif node.val < 0:
            self._rotate_left(node, abs(node.val) % n)

    @staticmethod
    def _rotate_right(node: Node, length: int) -> None:
        curr = node
        for _ in range(length):
            curr = curr.next
        CDLL.insert(curr, node)

    @staticmethod
    def _rotate_left(node: Node, length: int) -> None:
        curr = node
        for _ in range(length):
            curr = curr.prev
        CDLL.insert(curr.prev, node)

    def follow(self, nb_steps: int) -> int:
        n = nb_steps % self.n

        curr = self.head
        for _ in range(n):
            curr = curr.next
        return curr.val

    def show(self) -> None:
        print(self.head, end=" -> ")
        curr = self.head.next
        while curr != self.head:
            print(curr, end=" -> ")
            curr = curr.next
        print()


@Timer.timeit
def decrypt(
    array: List[int],
    decryption_key: int,
    nb_rounds: int,
    indexes: List[int] = [1000, 2000, 3000],
) -> int:
    cdll = CDLL([decryption_key * val for val in array])

    for _ in range(nb_rounds):
        for idx in range(len(array)):
            cdll.move(idx)

    return sum(cdll.follow(index) for index in indexes)


@Timer.timeit
def parse(filename: str) -> List[int]:
    with open(filename, "r") as file:
        array = list(map(int, file.read().strip().split("\n")))
    return array


@Timer.timeit
def solve(filename: str) -> Tuple[int, int]:
    array = parse(filename)
    part1 = decrypt(array, 1, 1)
    part2 = decrypt(array, 811589153, 10)

    return part1, part2


def main() -> None:
    import os

    res = solve(os.path.dirname(os.path.abspath(__file__)) + "/input.txt")

    assert res[0] == 6712, f"Part1 = {res[0]}"
    assert res[1] == 1595584274798, f"Part2 = {res[1]}"


if __name__ == "__main__":
    main()
