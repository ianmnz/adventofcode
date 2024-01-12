# Advent of Code : Day 02 - Cube Conundrum
# https://adventofcode.com/2023/day/2

import re
from typing import List, Dict, Tuple


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


def solve(filename: str) -> Tuple[int, int]:
    with open(filename, "r") as file:
        games = dict()
        for game in file.read().strip().split('\n'):
            game_id, subsets = game.split(':')
            games[int(re.findall(f'\d+', game_id)[0])] = [subset.split(',') for subset in subsets.split(';')]

    part1 = determine_possible_games(games)
    part2 = determine_minimum_power_set_cubes(games)

    return part1, part2


def main():
    import os
    from helpers import Timer

    with Timer():
        res = solve(os.path.dirname(os.path.abspath(__file__)) + "/input.txt")

        assert res[0] == 2162,  f"Part1 = {res[0]}"
        assert res[1] == 72513, f"Part2 = {res[1]}"


if __name__ == "__main__":
    main()
