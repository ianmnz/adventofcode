# Advent of Code : Day 01 - Calorie Counting
# https://adventofcode.com/2022/day/1

import collections
import operator


def main() -> None:
    elves = collections.defaultdict(int)

    with open("input.txt", 'r') as file:
        id_elf = 1
        for line in file:
            if line == '\n':
                id_elf += 1
            else:
                elves[id_elf] += int(line)


    elves = sorted(elves.items(), key=operator.itemgetter(1), reverse=True)

    # Answer part 1 :
    print(f"First elf: {elves[0][0]}") # 128
    print(f"Max calories: {elves[0][1]}") # 71934

    # --- Part 2 ---
    nb_elves = 3
    id_elves = []
    sum_calories = 0
    for i in range(nb_elves):
        id_elves.append(elves[i])
        sum_calories += elves[i][1]

    # Answer part 2 :
    print(f"First {nb_elves} elves: {id_elves}") # [(128, 71934), (27, 69849), (165, 69664)]
    print(f"Sum of first {nb_elves} max calories: {sum_calories}") # 211447


if __name__ == "__main__":
    main()
