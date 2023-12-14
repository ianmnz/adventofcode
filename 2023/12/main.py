# Advent of Code : Day 12 - Hot Springs
# https://adventofcode.com/2023/day/12

from typing import Tuple, List
from functools import lru_cache


def nb_arrangements(record: str, duplicate: Tuple[int]) -> int:

    @lru_cache(maxsize=None)
    def recursive(idx_r: int, idx_d: int) -> int:
        if len(record) == idx_r:
            # We arrived at the end of the record
            # Return 1 if we dealt with all blocks
            # 0 otherwise
            return int(len(duplicate) == idx_d)

        if record[idx_r] in '.?':
            # If current is a '.' or a '?'
            # it means we can keep advancing
            # until we find a '#' or reach the end
            result = recursive(idx_r + 1, idx_d)
        else:
            result = 0

        try:
            # Check the end of the block
            idx_r_last = idx_r + duplicate[idx_d]

            if '.' not in record[idx_r: idx_r_last] and record[idx_r_last] != '#':
                result += recursive(idx_r_last + 1, idx_d + 1)

        except IndexError:
            pass

        return result

    return recursive(0, 0)


def sum_arrangements(records: List[Tuple[str]]) -> int:
    ans = 0
    for record in records:
        ans += nb_arrangements(record[0] + '?', eval(record[1]))
    return ans


def sum_unfolded_arrangements(records: List[Tuple[str]]) -> int:
    ans = 0
    unfold = 5
    for record in records:
        ans += nb_arrangements((record[0] + '?') * unfold, eval(record[1]) * unfold)
    return ans


def main():
    import os
    import sys

    # To be able to import the helpers module
    sys.path.append(os.path.dirname(                                        # Project
                        os.path.dirname(                                    # Year
                            os.path.dirname(os.path.abspath(__file__)))))   # Day

    from helpers import Timer

    with open("input.txt", "r") as file:
        records = [tuple(line.split()) for line in file.read().split('\n')]

    # --- Part 1 --- #
    with Timer():
        print("Sum of arrangements:", sum_arrangements(records))  # 7460

    # --- Part 2 --- #
    with Timer():
        print("Sum of unfolded arrangements:", sum_unfolded_arrangements(records))  # 6720660274964


if __name__ == "__main__":
    main()
