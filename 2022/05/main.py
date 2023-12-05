# Advent of Code : Day 05 - Supply Stacks
# https://adventofcode.com/2022/day/5

import collections
from typing import Dict

class Cargo:
    cargo: Dict[int, collections.deque]

    def __init__(self, nb_stack: int) -> None:
        self.cargo = dict()
        for i in range(1, nb_stack + 1):
            self.cargo[i] = collections.deque()

    def append(self, stack: int, crate: str) -> None:
        self.cargo[stack].append(crate)

    def pop(self, stack: int) -> str:
        return self.cargo[stack].pop()

    def head(self, stack: int) -> str:
        return self.cargo[stack][-1]

    def show(self) -> None:
        for id, stack in self.cargo.items():
            print(id, ' : ', stack)

    def move1(self, nb_crates: int, from_stack: int, to_stack: int) -> None:
        for _ in range(nb_crates):
            crate = self.pop(from_stack)
            self.append(to_stack, crate)

    def move2(self, nb_crates: int, from_stack: int, to_stack: int) -> None:
        moved_crates = collections.deque()
        for _ in range(nb_crates):
            crate = self.pop(from_stack)
            moved_crates.append(crate)

        for _ in range(len(moved_crates)):
            crate = moved_crates.pop()
            self.append(to_stack, crate)

    @property
    def answer(self) -> str:
        answer = ''
        for id in self.cargo.keys():
            answer += self.head(id)
        return answer


def main():
    stacks = []
    moves = []

    with open('input.txt', 'r') as file:
        # Read initial cargo
        for line in file:
            if line == '\n':
                # Separates the initial stacks from
                # the moves
                break

            elif line.startswith(' '):
                # It implicitly considers that the first stack
                # is one of the biggest ones
                continue

            line = line.replace('    ', ' []').rstrip().split()
            stacks.append([crate.rstrip(']').lstrip('[') for crate in line])

        # Read moves
        # Since variable 'file' is a generator
        # it picks up from the last read line
        for line in file:
            line = line.strip().split()

            nb_crates = int(line[1])
            from_stack = int(line[3])
            to_stack = int(line[5])

            moves.append((nb_crates, from_stack, to_stack))

    # Initialize cargos
    cargo1 = Cargo(len(stacks[0])) # Answer 1
    cargo2 = Cargo(len(stacks[0])) # Answer 2

    for row in reversed(stacks):
        for stack, crate in enumerate(row, start=1):
            if crate != '':
                cargo1.append(stack, crate)
                cargo2.append(stack, crate)

    # cargo1.show()

    # Move crates
    for nb_crates, from_stack, to_stack in moves:
        cargo1.move1(nb_crates, from_stack, to_stack)
        cargo2.move2(nb_crates, from_stack, to_stack)

    # cargo1.show()
    # cargo2.show()

    # Answer part 1 :
    print(f'Head of crates for CraneMover9000: {cargo1.answer}') # QNNTGTPFN

    # Answer part 2 :
    print(f'Head of crates for CraneMover9001: {cargo2.answer}') # GGNPJBTTR


if __name__ == "__main__":
    main()