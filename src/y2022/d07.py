# Advent of Code : Day 07 - No Space Left On Device
# https://adventofcode.com/2022/day/7

import os
from dataclasses import dataclass, field
from functools import cached_property
from typing import Dict, List, Optional, Tuple

from helpers import Timer


@dataclass
class File:
    name: str
    du: int


@dataclass
class Dir:
    name: str
    parent: Optional["Dir"] = field(default=None)
    children: Dict[str, "Dir"] = field(init=False, default_factory=dict)
    files: List[File] = field(init=False, default_factory=list)

    def cd(self, child_name: str) -> "Dir":
        return self.children[child_name]

    def mkdir(self, child_name: str) -> "Dir":
        child = Dir(child_name, self)
        self.children[child_name] = child
        return child

    def touch(self, file_name: str, file_size: int) -> File:
        file = File(file_name, file_size)
        self.files.append(file)
        return file

    @cached_property
    def du(self) -> int:
        # Recursively computes the size of the directory
        return sum(file.du for file in self.files) + sum(
            child.du for child in self.children.values()
        )


@Timer.timeit
def build_filesystem(terminal_output: List[str]) -> Dir:
    outermost_dir = Dir("/")
    current_dir = outermost_dir

    for line in terminal_output:
        parsed_line = line.split()

        if current_dir is None:
            break

        if parsed_line[0] == "$":  # Command
            if parsed_line[1] == "cd":  # Cd
                if parsed_line[2] == "/":
                    current_dir = outermost_dir

                elif parsed_line[2] == "..":
                    current_dir = current_dir.parent

                else:
                    current_dir = current_dir.cd(parsed_line[2])

            elif parsed_line[1] == "ls":
                continue

        else:  # Listing
            if parsed_line[0] == "dir":
                current_dir.mkdir(parsed_line[1])

            elif parsed_line[0].isnumeric():
                current_dir.touch(parsed_line[1], int(parsed_line[0]))

    return outermost_dir


@Timer.timeit
def sum_dir_sizes_leq_threshold(root: Dir, size_max: int = 100_000) -> int:
    sum_dir_total_size_leq_n = 0

    dirs = [root]
    while dirs:
        curr = dirs.pop()

        if curr.du <= size_max:
            sum_dir_total_size_leq_n += curr.du

        for child in curr.children.values():
            dirs.append(child)

    return sum_dir_total_size_leq_n


@Timer.timeit
def find_size_smallest_dir_to_be_deleted(
    root: Dir, total_disk_space: int = 70_000_000, needed_space: int = 30_000_000
) -> int:
    total_used_space = root.du
    total_unused_space = total_disk_space - total_used_space
    space_to_be_freed = needed_space - total_unused_space

    if space_to_be_freed <= 0:
        return 0

    smallest_dir_to_be_deleted_size = total_used_space

    dirs = [root]
    while dirs:
        curr = dirs.pop()

        if space_to_be_freed <= curr.du < smallest_dir_to_be_deleted_size:
            smallest_dir_to_be_deleted_size = curr.du

        for child in curr.children.values():
            dirs.append(child)

    return smallest_dir_to_be_deleted_size


@Timer.timeit
def parse(filename: os.PathLike) -> List[str]:
    with open(filename, "r") as file:
        terminal_output = file.read().strip().split("\n")
    return terminal_output


@Timer.timeit
def solve(filename: os.PathLike) -> Tuple[int, int]:
    terminal_output = parse(filename)
    root = build_filesystem(terminal_output)
    part1 = sum_dir_sizes_leq_threshold(root)
    part2 = find_size_smallest_dir_to_be_deleted(root)

    return part1, part2


def main() -> None:
    from pathlib import Path

    res = solve(Path(__file__).parent / "input.txt")

    assert res[0] == 1454188, f"Part1 = {res[0]}"
    assert res[1] == 4183246, f"Part2 = {res[1]}"


if __name__ == "__main__":
    main()
