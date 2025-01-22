# Advent of Code : Day 11 - Monkey in the Middle
# https://adventofcode.com/2022/day/11

import copy
import functools
import operator
import re
from dataclasses import dataclass, field
from typing import Callable, Self

from helpers import Timer, load_input_data


@dataclass
class WorryEval:
    func: Callable[[int], int]
    relief_factor: int = field(init=False, default=3)
    mod_factor: int = field(init=False, default=int(1.0e7))

    def __call__(self, x: int) -> int:
        return (self.func(x) // self.relief_factor) % self.mod_factor


@dataclass(frozen=True)
class Decision:
    divisor: int
    send_if_divisible: int
    send_if_not_divisible: int

    def send_to(self, item: int) -> int:
        return (
            self.send_if_not_divisible
            if item % self.divisor
            else self.send_if_divisible
        )


@dataclass
class Monkey:
    id: int

    worry_eval: None | WorryEval = field(init=False, default=None)
    decision: None | Decision = field(init=False, default=None)

    items: list[int] = field(init=False, default_factory=list)
    nb_inspected_items: int = field(init=False, default=0)

    def receive_item(self, item: int) -> None:
        self.items.append(item)

    def inspect_items(self, monkeys: dict[int, Self]) -> None:
        for item in self.items:
            item = self.worry_eval(item)
            send_to = self.decision.send_to(item)
            monkeys[send_to].receive_item(item)

        self.nb_inspected_items += len(self.items)
        self.items = []


@Timer.timeit
def update_worry_evaluation(monkeys: dict[int, Monkey], relief_factor: int = 1) -> None:
    mod = functools.reduce(
        operator.mul, (monkey.decision.divisor for monkey in monkeys.values())
    )
    for monkey in monkeys.values():
        monkey.worry_eval.relief_factor = relief_factor
        monkey.worry_eval.mod_factor = mod


@Timer.timeit
def compute_monkey_business(nb_rounds: int, monkeys: dict[int, Monkey]) -> int:
    for _ in range(nb_rounds):
        for monkey in monkeys.values():
            monkey.inspect_items(monkeys)

    most_active_monkeys = sorted(
        (monkey.nb_inspected_items for monkey in monkeys.values()), reverse=True
    )
    return most_active_monkeys[0] * most_active_monkeys[1]


@Timer.timeit
def parse(data: str) -> dict[int, Monkey]:
    notes = data.strip().split("\n\n")

    monkey_id = re.compile(r"Monkey (\d+):")
    items = re.compile(r"Starting items: (.*)")
    operation = re.compile(r"Operation: new = (.*)")
    divisor = re.compile(r"divisible by (\d+)")
    throw_to_if_true = re.compile(r"If true: throw to monkey (\d+)")
    throw_to_if_false = re.compile(r"If false: throw to monkey (\d+)")

    monkeys = {}
    for note in notes:
        match = monkey_id.search(note)

        if match is None:
            continue

        monkey = Monkey(int(match.group(1)))

        match = items.search(note)
        for worry in match.group(1).split():
            monkey.receive_item(int(worry.rstrip(",")))

        match = operation.search(note)
        monkey.worry_eval = WorryEval(eval(f"lambda old: {match.group(1)}"))

        match = divisor.search(note)
        div = int(match.group(1))
        match = throw_to_if_true.search(note)
        send_if_true = int(match.group(1))
        match = throw_to_if_false.search(note)
        send_if_false = int(match.group(1))

        monkey.decision = Decision(div, send_if_true, send_if_false)

        monkeys[monkey.id] = monkey

    return monkeys


@Timer.timeit
def solve(data: str) -> tuple[int, int]:
    monkeys = parse(data)
    monkeys_cp = copy.deepcopy(monkeys)
    update_worry_evaluation(monkeys_cp)

    part1 = compute_monkey_business(20, monkeys)
    part2 = compute_monkey_business(10_000, monkeys_cp)

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2022, 11)))
