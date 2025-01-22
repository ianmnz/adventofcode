# Advent of Code : Day 12 - Hot Springs
# https://adventofcode.com/2023/day/12
#
# For some more explanation
# https://www.reddit.com/r/adventofcode/comments/18ghux0/comment/kd0npmi/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button

from functools import lru_cache

from helpers import Timer, load_input_data


def nb_arrangements(record: str, duplicate: tuple[int]) -> int:
    @lru_cache(maxsize=None)
    def recursive(idx_r: int, idx_d: int) -> int:
        if len(record) == idx_r:
            # We arrived at the end of the record
            # Return 1 if we dealt with all blocks
            # 0 otherwise
            return int(len(duplicate) == idx_d)

        if record[idx_r] in ".?":
            # If current is a '.' or a '?'
            # it means we can keep advancing
            # until we find a '#' or reach the end
            result = recursive(idx_r + 1, idx_d)
        else:
            result = 0

        try:
            # Check the end of the block
            idx_r_last = idx_r + duplicate[idx_d]

            if "." not in record[idx_r:idx_r_last] and record[idx_r_last] != "#":
                result += recursive(idx_r_last + 1, idx_d + 1)

        except IndexError:
            pass

        return result

    return recursive(0, 0)


@Timer.timeit
def sum_arrangements(records: list[tuple[str, ...]]) -> int:
    ans = 0
    for record in records:
        ans += nb_arrangements(record[0] + "?", eval(record[1]))
    return ans


@Timer.timeit
def sum_unfolded_arrangements(records: list[tuple[str, ...]]) -> int:
    ans = 0
    unfold = 5
    for record in records:
        ans += nb_arrangements((record[0] + "?") * unfold, eval(record[1]) * unfold)
    return ans


@Timer.timeit
def parse(data: str) -> list[tuple[str, ...]]:
    return [tuple(line.split()) for line in data.split("\n")]


@Timer.timeit
def solve(data: str) -> tuple[int, int]:
    records = parse(data)
    part1 = sum_arrangements(records)
    part2 = sum_unfolded_arrangements(records)

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2023, 12)))
