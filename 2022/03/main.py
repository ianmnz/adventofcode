# Advent of Code : Day 03 - Rucksack Reorganization
# https://adventofcode.com/2022/day/3


def priority(item: str) -> int:
    prio = {
        'a' :  1,
        'b' :  2,
        'c' :  3,
        'd' :  4,
        'e' :  5,
        'f' :  6,
        'g' :  7,
        'h' :  8,
        'i' :  9,
        'j' : 10,
        'k' : 11,
        'l' : 12,
        'm' : 13,
        'n' : 14,
        'o' : 15,
        'p' : 16,
        'q' : 17,
        'r' : 18,
        's' : 19,
        't' : 20,
        'u' : 21,
        'v' : 22,
        'w' : 23,
        'x' : 24,
        'y' : 25,
        'z' : 26
    }
    if item.isupper():
        return 26 + prio[item.lower()]
    else:
        return prio[item]

def main() -> None:
    sum_common_type_prio = 0
    sum_badge_type_prio = 0

    with open('input.txt', 'r') as file:
        for count, line in enumerate(file):
            line = line.strip()
            compartment_size = len(line)//2

            # --- Part 1 ---
            first_compartment = set(line[:compartment_size])
            second_compartment = set(line[compartment_size:])

            common_type = list(first_compartment.intersection(second_compartment))[0]
            sum_common_type_prio += priority(common_type)

            # --- Part 2 ---
            elf_badge = set(line)

            if count % 3 == 0:
                group_badge = elf_badge
            else:
                group_badge = group_badge.intersection(elf_badge)

                if count % 3 == 2:
                    badge_type = list(group_badge)[0]
                    sum_badge_type_prio += priority(badge_type)

    # Answer part 1 :
    print(f"Sum of common type priorities: {sum_common_type_prio}") # 8515

    # Answer part 2 :
    print(f"Sum of badge type priorities: {sum_badge_type_prio}") # 2434

if __name__ == "__main__":
    main()