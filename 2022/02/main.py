# Advent of Code : Day 02 - Rock Paper Scissors
# https://adventofcode.com/2022/day/2


score_part1 = { 'A' : {'X' : 4, 'Y': 8, 'Z': 3},
                'B' : {'X' : 1, 'Y': 5, 'Z': 9},
                'C' : {'X' : 7, 'Y': 2, 'Z': 6} }


score_part2 = { 'A' : {'X' : 3, 'Y': 4, 'Z': 8},
                'B' : {'X' : 1, 'Y': 5, 'Z': 9},
                'C' : {'X' : 2, 'Y': 6, 'Z': 7} }


def main() -> None:
    total_score_part1 = 0
    total_score_part2 = 0

    with open('input.txt', 'r') as file:
        for line in file:
            opponent, player = line.split()
            total_score_part1 += score_part1[opponent][player]
            total_score_part2 += score_part2[opponent][player]

    # Answer part 1 :
    print(f'Total score: {total_score_part1}') # 11873

    # Answer part 2 :
    print(f'Total score: {total_score_part2}') # 12014


if __name__ == "__main__":
    main()