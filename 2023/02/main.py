# Advent of Code : Day 02 - Cube Conundrum
# https://adventofcode.com/2023/day/2

import re
from typing import List, Dict


def determine_possible_games(games: Dict[int, List[str]]) -> int:
    sum_possible_games = 0

    N_R = 12
    N_G = 13
    N_B = 14

    def is_game_possible(game: List[List[str]]) -> bool:
        for subset in game:
            for cubes in subset:
                n, color = cubes.split()
                n = int(n)

                if (color == 'red') and (n > N_R):
                    return False
                elif (color == 'green') and (n > N_G):
                    return False
                elif (color == 'blue') and (n > N_B):
                    return False

        return True


    for game_id, game in games.items():
        if is_game_possible(game):
            sum_possible_games += game_id

    return sum_possible_games


def determine_minimum_power_set_cubes(games: Dict[int, List[str]]) -> int:
    sum_power_set_cubes = 0

    def minimum_possible_game_power(game: List[List[str]]) -> int:
        R = G = B = 1

        for subset in game:
            for cubes in subset:
                n, color = cubes.split()
                n = int(n)

                if (color == 'red'):
                    R = max(R, n)
                elif (color == 'green'):
                    G = max(G, n)
                elif (color == 'blue'):
                    B = max(B, n)

        return R * G * B


    for game in games.values():
        sum_power_set_cubes += minimum_possible_game_power(game)

    return sum_power_set_cubes


def main():
    import os
    import sys

    # To be able to import the helpers module
    sys.path.append(os.path.dirname(                                        # Project
                        os.path.dirname(                                    # Year
                            os.path.dirname(os.path.abspath(__file__)))))   # Day

    from helpers import Timer

    with open("input.txt", "r") as file:
        games = dict()
        for game in file.read().strip().split('\n'):
            game_id, subsets = game.split(':')
            games[int(re.findall(f'\d+', game_id)[0])] = [subset.split(',') for subset in subsets.split(';')]

    # --- Part 1 --- #
    with Timer():
        print("Sum of IDs of all possible games:", determine_possible_games(games)) # 2162

    # --- Part 2 --- #
    with Timer():
        print("Sum of minimum power set cubes:", determine_minimum_power_set_cubes(games)) # 72513


if __name__ == "__main__":
    main()
