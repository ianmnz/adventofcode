# Advent of Code : Day 09 - Rope Bridge
# https://adventofcode.com/2022/day/9


from typing import Set, Tuple
import numpy as np


class RopeKnot:
    _right = np.array([1, 0])
    _left = -1 * _right
    _up = np.array([0, 1])
    _down = -1 * _up

    def __init__(self, start: np.array = np.array([0, 0])) -> None:
        self._position: np.array = start
        self._visited: Set[Tuple[int, int]] = {tuple(start)}

    def move(self, dir_str: str) -> None:
        direction = np.array([0, 0])

        if 'L' in dir_str:
            direction += self._left
        if 'R' in dir_str:
            direction += self._right
        if 'U' in dir_str:
            direction += self._up
        if 'D' in dir_str:
            direction += self._down

        self._position = self._position + direction
        self._visited.add(tuple(self._position))

    def follow(self, other: 'RopeKnot') -> None:
        if self._is_adjacent(other):
            return

        x, y = self._relative_position(other)

        if x * y == 0: # Same row or column
            if x > 0:
                self.move('R')
            elif x < 0:
                self.move('L')
            elif y > 0:
                self.move('U')
            elif y < 0:
                self.move('D')

        else: # Diagonally
            if x * y > 0:
                if x > 0: # to 1st quadrant
                    self.move('RU')
                else: # to 3rd quadrant
                    self.move('LD')

            elif x * y < 0:
                if x > 0: # to 2nd quadrant
                    self.move('RD')
                else: # to 4th quadrant
                    self.move('LU')

    def _relative_position(self, other: 'RopeKnot') -> Tuple[int, int]:
        x = other._position[0] - self._position[0]
        y = other._position[1] - self._position[1]
        return x, y

    def _is_adjacent(self, other: 'RopeKnot') -> bool:
        x, y = self._relative_position(other)
        return abs(x) <= 1 and abs(y) <= 1


class Rope:
    def __init__(self, nb_knots: int, start: np.array = np.array([0, 0])) -> None:
        self._knots = [RopeKnot(start) for _ in range(nb_knots)]
        self._head = self._knots[0]
        self._tail = self._knots[nb_knots-1]

    def move(self, dir_str: str, dist: int) -> None:
        for _ in range(dist):
            self._head.move(dir_str)
            for i in range(1, len(self._knots)):
                self._knots[i].follow(self._knots[i-1])


def main():
    rope_part1 = Rope(2)
    rope_part2 = Rope(10)

    nb_positions_tail_visited_part1 = 0
    nb_positions_tail_visited_part2 = 0

    with open('input.txt', 'r') as file:
        for line in file:
            line = line.strip().split()

            dir_str = line[0]
            dist = int(line[1])

            rope_part1.move(dir_str, dist)
            rope_part2.move(dir_str, dist)

    nb_positions_tail_visited_part1 = len(rope_part1._tail._visited)
    nb_positions_tail_visited_part2 = len(rope_part2._tail._visited)

    # Answer part 1 :
    print(f'Number of positions Tail visited (part 1): {nb_positions_tail_visited_part1}') # 6197

    # Answer part 2 :
    print(f'Number of positions Tail visited (part 2): {nb_positions_tail_visited_part2}') # 2562


if __name__ == "__main__":
    main()