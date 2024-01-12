# Advent of Code : Day 15 - Lens Library
# https://adventofcode.com/2023/day/15

from typing import List, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class LensSlot:
    label: int
    focal:  int
    next: Optional['LensSlot'] = field(default=None, init=False)


class Box:
    head: LensSlot

    def __init__(self) -> None:
        self.head = None

    def remove(self, label: int) -> None:
        if self.head is None:
            return

        if self.head.label == label:
            self.head = self.head.next
            return

        curr = self.head.next
        prev = self.head

        while curr is not None:
            if curr.label == label:
                prev.next = curr.next
                curr.next = None
                return

            prev = curr
            curr = curr.next

    def insert(self, label: int, focal: int) -> None:
        if self.head is None:
            self.head = LensSlot(label, focal)
            return

        curr = self.head
        prev = None
        while curr is not None:
            if curr.label == label:
                curr.focal = focal
                return

            prev = curr
            curr = curr.next
        prev.next = LensSlot(label, focal)

    def focusing_power(self) -> int:
        power = 0
        count = 1
        curr = self.head

        while curr is not None:
            power += count * curr.focal
            curr = curr.next
            count += 1
        return power


def HASH(string: str) -> int:
    curr = 0
    for char in string:
        curr += ord(char)
        curr *= 17
        curr %= 256
    return curr


def HASHMAP(string: str, boxes: List[Box]) -> List[Box]:
    if '-' in string:
        label, _ = string.split('-')
        boxes[HASH(label)].remove(label)

    else:
        label, focal = string.split('=')
        boxes[HASH(label)].insert(label, int(focal))

    return boxes


def verify_HASH(sequence: List[str]) -> int:
    return sum(HASH(string) for string in sequence)


def verify_HASHMAP(sequence: List[str]) -> int:
    boxes = [Box() for _ in range(256)]
    for string in sequence:
        boxes = HASHMAP(string, boxes)

    return sum(idx * box.focusing_power() for idx, box in enumerate(boxes, 1))


def solve(filename: str) -> Tuple[int, int]:
    with open(filename, "r") as file:
        sequence = file.read().strip().split(',')

    part1 = verify_HASH(sequence)
    part2 = verify_HASHMAP(sequence)

    return part1, part2


def main():
    import os
    from helpers import Timer

    with Timer():
        res = solve(os.path.dirname(os.path.abspath(__file__)) + "/input.txt")

        assert res[0] == 510792, f"Part1 = {res[0]}"
        assert res[1] == 269410, f"Part2 = {res[1]}"


if __name__ == "__main__":
    main()
