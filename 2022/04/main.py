# Advent of Code : Day 04 - Camp Cleanup
# https://adventofcode.com/2022/day/4


def main() -> None:
    nb_fully_contained_ranges = 0
    nb_overlaped_not_fully_contained_ranges = 0

    with open('input.txt', 'r') as file:
        for line in file:
            first_range, second_range = line.strip().split(',')

            first_lower, first_upper = [int(bound) for bound in first_range.split('-')]
            second_lower, second_upper = [int(bound) for bound in second_range.split('-')]

            if ((first_lower <= second_lower) and (second_upper <= first_upper)) or \
               ((second_lower <= first_lower) and (first_upper <= second_upper)):
                nb_fully_contained_ranges += 1

            elif (first_lower <= second_lower <= first_upper) or \
                 (second_lower <= first_lower <= second_upper):
                nb_overlaped_not_fully_contained_ranges += 1

    # Answer part 1 :
    print(f"Number of fully contained assigment pairs: {nb_fully_contained_ranges}") # 528

    # Answer part 2 :
    print(f"Number of overlaped assigment pairs: {nb_fully_contained_ranges + nb_overlaped_not_fully_contained_ranges}") # 881


if __name__ == "__main__":
    main()