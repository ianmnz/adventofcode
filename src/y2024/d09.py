# Advent of Code : Day 09 - Disk Fragmenter
# https://adventofcode.com/2024/day/09

import heapq
from collections import defaultdict

from helpers import Timer, load_input_data


@Timer.timeit
def individual_defragment(files: list[tuple], gaps: list[tuple]) -> list[tuple]:
    used_space = files[::]
    free_space = gaps[::-1]

    moved = []
    while True:
        gap_pos, gap_len = free_space.pop()
        file_pos, file_len, file_id = used_space.pop()

        if gap_pos > file_pos:
            used_space.append((file_pos, file_len, file_id))
            break

        if gap_len >= file_len:
            moved.append((gap_pos, file_len, file_id))  # Moved file completely

            if gap_len > file_len:
                free_space.append((gap_pos + file_len, gap_len - file_len))

        else:
            moved.append((gap_pos, gap_len, file_id))  # Moved file partially
            used_space.append((file_pos, file_len - gap_len, file_id))

    return used_space + moved


@Timer.timeit
def block_defragment(files: list[tuple], gaps: list[tuple]) -> list[tuple]:
    blocks = {file_id: (pos, length) for pos, length, file_id in files}

    free_space = defaultdict(list)
    for pos, length in gaps:
        heapq.heappush(free_space[length], pos)

    for file_id in reversed(blocks):
        file_pos, file_len = blocks[file_id]

        spans = [
            (gap_positions[0], gap_len)
            for gap_len, gap_positions in free_space.items()
            if gap_len >= file_len
        ]

        if not spans:
            continue

        gap_pos, gap_len = min(spans)

        if file_pos <= gap_pos:
            continue

        blocks[file_id] = (gap_pos, file_len)  # Moved whole file
        heapq.heappop(free_space[gap_len])  # Filled gap partially or completely

        if not free_space[gap_len]:
            del free_space[gap_len]

        if remaining_gap_len := gap_len - file_len:
            heapq.heappush(free_space[remaining_gap_len], gap_pos + file_len)

    return [(pos, length, file_id) for file_id, (pos, length) in blocks.items()]


@Timer.timeit
def filesystem_checksum(disk: list[tuple]) -> int:
    # pos * id + (pos + 1)*id + ... + (pos + len - 1) * id =
    # id * [pos + (pos + 1) + ... + (pos + len - 1)] =
    # id * [len * pos + 0 + 1 + ... + (len - 1)] =
    # id * [len * pos + (len - 1) * len / 2] =
    # id * len * [pos + (len - 1) / 2]
    return int(
        sum(
            file_id * length * (pos + (length - 1) / 2) for pos, length, file_id in disk
        )
    )


@Timer.timeit
def parse(data: str) -> tuple[list[tuple], list[tuple]]:
    files = []
    gaps = []

    pos = 0
    for i, digit in enumerate(data):
        length = int(digit)

        if i % 2 == 0:
            files.append((pos, length, i // 2))

        elif length > 0:
            gaps.append((pos, length))

        pos += length

    return files, gaps


@Timer.timeit
def solve(data: str) -> tuple[int, int]:
    files, gaps = parse(data)
    part1 = filesystem_checksum(individual_defragment(files, gaps))
    part2 = filesystem_checksum(block_defragment(files, gaps))

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2024, 9)))
