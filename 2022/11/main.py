# Advent of Code : Day 11 - Monkey in the Middle
# https://adventofcode.com/2022/day/11

# CAN BE IMPROVED :
# PARSE CAN BE DONE BY YAML READER
# THE DATE STRUCTURE CAN BE LIGHTER

import collections
import operator
from typing import List, Dict, Callable


class Item:
    def __init__(self, id: int, val: int) -> None:
        self.id = id
        self.worry = val


class Monkey:
    def __init__(self, id: int) -> None:
        self.id: int = id
        self.items: List[Item] = []
        self.operator: Callable[[int], int] = None
        self.probe: int = -1
        self.true: int = -1
        self.false: int = -1

    def add_item(self, item: Item) -> None:
        self.items.append(item)

    def inspect(self, monkeys: Dict[int, 'Monkey'], mod: int = 1) -> None:
        for item in self.items:
            item.worry = self.operator(item.worry)
            # item.worry = item.worry // 3
            item.worry = item.worry % mod

            if item.worry % self.probe == 0:
                to_monkey = monkeys[self.true]
            else:
                to_monkey = monkeys[self.false]

            to_monkey.add_item(item)

        self.items = []


def round(monkeys: Dict[int, Monkey], nb_inspected_items_by_monkey: Dict[int, int], mod: int = 1) -> None:
    for monkey_id, monkey in monkeys.items():
        nb_inspected_items_by_monkey[monkey_id] += len(monkey.items)
        monkey.inspect(monkeys, mod)


def main():
    monkeys: Dict[int, Monkey] = dict()
    count_items = 0
    curr_monkey = None
    # nb_rounds = 20
    nb_rounds = 10000

    nb_inspected_items_by_monkey: Dict[int, int] = collections.defaultdict(int)
    monkey_business = 0

    with open('input.txt', 'r') as file:
        for line in file:
            line = line.strip().split()

            if not line:
                continue

            elif line[0] == "Monkey":
                monkey_id = int(line[1].strip(':'))
                curr_monkey = Monkey(monkey_id)
                monkeys[monkey_id] = curr_monkey

            elif line[0] == "Starting":
                for i in range(2, len(line)):
                    item = Item(count_items, int(line[i].strip(',')))
                    curr_monkey.add_item(item)
                    count_items += 1

            elif line[0] == "Operation:":
                if line[4] == '+':
                    if line[5].isnumeric():
                        func = lambda old, val=int(line[5]) : old + val
                    else:
                        func = lambda old : old + old

                elif line[4] == '*':
                    if line[5].isnumeric():
                        func = lambda old, val=int(line[5]) : old * val
                    else:
                        func = lambda old : old * old

                curr_monkey.operator = func

            elif line[0] == "Test:":
                probe = int(line[3])
                curr_monkey.probe = probe

            elif line[1] == "true:":
                to_monkey_id = int(line[5])
                curr_monkey.true = to_monkey_id

            elif line[1] == "false:":
                to_monkey_id = int(line[5])
                curr_monkey.false = to_monkey_id

    mod = 1
    for monkey in monkeys.values():
        mod *= monkey.probe

    for _ in range(nb_rounds):
        round(monkeys, nb_inspected_items_by_monkey, mod)

    sorted_dict = sorted(nb_inspected_items_by_monkey.items(), key=operator.itemgetter(1), reverse=True)
    monkey_business = sorted_dict[0][1] * sorted_dict[1][1]
    # print(nb_inspected_items_by_monkey)
    # print(sorted_dict)

    # Answer part 1 : nb_rounds = 20
    print(f'The two most active monkeys: {sorted_dict[0][0]}, {sorted_dict[1][0]}') # 5, 3
    print(f'Number of inspections of the 2 most active monkeys: {sorted_dict[0][1]}, {sorted_dict[1][1]}') # 358, 308
    print(f'Monkey business: {monkey_business}') # 110264

    # Answer part 2 : nb_rounds = 10'000
    print(f'The two most active monkeys: {sorted_dict[0][0]}, {sorted_dict[1][0]}') # 5, 3
    print(f'Number of inspections of the 2 most active monkeys: {sorted_dict[0][1]}, {sorted_dict[1][1]}') # 168658, 140002
    print(f'Monkey business: {monkey_business}') # 23612457316


if __name__ == "__main__":
    main()