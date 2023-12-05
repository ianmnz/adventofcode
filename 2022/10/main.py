# Advent of Code : Day 10 - Cathode-Ray Tube
# https://adventofcode.com/2022/day/10


def main():
    instruction = {
                    'noop': 1,
                    'addx': 2
                  }

    cycles_of_interest = [20, 60, 100, 140, 180, 220]

    CRT_WIDTH = 40
    CRT_HEIGHT = 6
    crt = [["." for _ in range(CRT_WIDTH)] for _ in range(CRT_HEIGHT)]

    sum_signal_strength_on_cycles_of_interest = 0

    cycle_counter = 1
    register = 1

    sprite_width = 3

    with open('input.txt', 'r') as file:
        for line in file:
            line = line.strip().split()

            for cycle in range(instruction.get(line[0], 0)):
                if cycle_counter in cycles_of_interest:
                    sum_signal_strength_on_cycles_of_interest += cycle_counter * register

                i = (cycle_counter - 1) // CRT_WIDTH
                j = (cycle_counter - 1) % CRT_WIDTH

                if (register - (sprite_width // 2)) <= j <= (register + (sprite_width // 2)):
                    crt[i][j] = "#"

                if line[0] == 'addx' and cycle + 1 == instruction['addx']:
                    register += int(line[1])

                cycle_counter += 1


    # Answer part 1 :
    print(f'Sum of signal strengths: {sum_signal_strength_on_cycles_of_interest}') # 15020

    # Answer part 2
    # It should print EFUGLPAP
    for i in range(CRT_HEIGHT):
        for j in range(CRT_WIDTH):
            print(crt[i][j], end='')
        print()



if __name__ == "__main__":
    main()