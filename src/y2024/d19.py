# Advent of Code : Day 19 - Linen Layout
# https://adventofcode.com/2024/day/19

from functools import cache, partial

from helpers import Timer, load_input_data


def count_nb_arrangements(patterns: list[str], design: str) -> int:
    @cache
    def _count(design: str):
        if not design:
            return 1

        return sum(
            _count(pruned)
            for p in patterns
            if (pruned := design.removeprefix(p)) != design
        )

    return _count(design)


@Timer.timeit
def count_designs(patterns: list[str], designs: list[str]) -> tuple[int, int]:
    res = list(map(partial(count_nb_arrangements, patterns), designs))
    return sum(map(lambda x: x > 0, res)), sum(res)


@Timer.timeit
def parse(data: str) -> tuple[list[str], list[str]]:
    patterns, designs = data.split("\n\n")
    return (
        sorted(patterns.split(", ")),
        designs.splitlines(),
    )


@Timer.timeit
def solve(data: str) -> tuple[int, int]:
    patterns, designs = parse(data)
    part1, part2 = count_designs(patterns, designs)

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2024, 19)))
