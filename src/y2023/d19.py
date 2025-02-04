# Advent of Code : Day 19 - Aplenty
# https://adventofcode.com/2023/day/19

import re
from itertools import islice

from helpers import Timer, load_input_data


def is_accepted(part: list[int], workflows: dict[str, str], start: str = "in") -> bool:
    x, m, a, s = part
    rules = workflows[start]

    for rule in rules.split(","):
        if ":" not in rule:
            if rule == "R":
                return False

            elif rule == "A":
                return True

            else:  # The last rule
                return is_accepted(part, workflows, rule)

        else:
            condition, destination = rule.split(":")
            if eval(condition):
                if destination == "R":
                    return False

                elif destination == "A":
                    return True

                else:
                    return is_accepted(part, workflows, destination)


def get_acceptance_range(
    parts_range: dict[str, tuple[int]], workflows: dict[str, str], start: str = "in"
) -> list[tuple[str, tuple[int]]]:
    rules = workflows.get(start, start)
    intervals = []

    for rule in rules.split(","):
        if ":" not in rule:
            if rule == "R":
                continue

            elif rule == "A":
                intervals.extend(parts_range.items())

            else:
                intervals.extend(get_acceptance_range(parts_range, workflows, rule))

        else:
            condition, destination = rule.split(":")
            category = condition[0]
            left, right = parts_range[category]
            is_gt = ">" == condition[1]
            threshold = int(condition[2:])

            # Accepted entirely
            if (is_gt and left > threshold) or (not is_gt and right < threshold):
                intervals.extend(
                    get_acceptance_range(parts_range, workflows, destination)
                )

            # Rejected entirely
            elif (is_gt and right < threshold) or (not is_gt and left > threshold):
                continue

            # Partially accepted
            else:
                accepted_parts_range = parts_range.copy()
                accepted_parts_range[category] = (
                    (threshold + 1, right) if is_gt else (left, threshold - 1)
                )
                parts_range[category] = (
                    (left, threshold) if is_gt else (threshold, right)
                )
                intervals.extend(
                    get_acceptance_range(accepted_parts_range, workflows, destination)
                )

    return intervals


@Timer.timeit
def sum_accepted_parts_rating(parts: list[list[int]], workflows: dict[str, str]) -> int:
    return sum([sum(part) for part in parts if is_accepted(part, workflows)])


@Timer.timeit
def nb_of_combinations_accepted(
    parts_range: dict[str, tuple[int]], workflows: dict[str, str]
) -> int:
    def batched(iterable, chunk_size):
        iterator = iter(iterable)
        while chunk := tuple(islice(iterator, chunk_size)):
            yield chunk

    nb_combinations = 0
    for batch in batched(get_acceptance_range(parts_range, workflows), len("xmas")):
        prod = 1
        for _, interval in batch:
            left, right = interval
            prod *= right - left + 1
        nb_combinations += prod
    return nb_combinations


@Timer.timeit
def parse(data: str) -> tuple[str, dict[str, str]]:
    temp, parts = data.split("\n\n")

    workflows = dict()
    for workflow in temp.split("\n"):
        name, rules = workflow.split("{")
        workflows[name] = rules[:-1]

    return parts, workflows


@Timer.timeit
def solve(data: str) -> tuple[int, int]:
    parts, workflows = parse(data)

    parts = [list(map(int, re.findall(r"\d+", part))) for part in parts.split("\n")]
    part1 = sum_accepted_parts_rating(parts, workflows)

    parts_range = {char: (1, 4000) for char in "xmas"}
    part2 = nb_of_combinations_accepted(parts_range, workflows)

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2023, 19)))
