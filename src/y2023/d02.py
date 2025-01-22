# Advent of Code : Day 02 - Cube Conundrum
# https://adventofcode.com/2023/day/2

import re

from helpers import Timer, load_input_data


@Timer.timeit
def determine_possible_games(games: dict[int, list[list[str]]]) -> int:
    sum_possible_games = 0

    N_R = 12
    N_G = 13
    N_B = 14

    def is_game_possible(game: list[list[str]]) -> bool:
        for subset in game:
            for cubes in subset:
                n, color = cubes.split()
                n = int(n)

                if (color == "red") and (n > N_R):
                    return False
                elif (color == "green") and (n > N_G):
                    return False
                elif (color == "blue") and (n > N_B):
                    return False

        return True

    for game_id, game in games.items():
        if is_game_possible(game):
            sum_possible_games += game_id

    return sum_possible_games


@Timer.timeit
def determine_minimum_power_set_cubes(games: dict[int, list[list[str]]]) -> int:
    sum_power_set_cubes = 0

    def minimum_possible_game_power(game: list[list[str]]) -> int:
        R = G = B = 1

        for subset in game:
            for cubes in subset:
                n, color = cubes.split()
                n = int(n)

                if color == "red":
                    R = max(R, n)
                elif color == "green":
                    G = max(G, n)
                elif color == "blue":
                    B = max(B, n)

        return R * G * B

    for game in games.values():
        sum_power_set_cubes += minimum_possible_game_power(game)

    return sum_power_set_cubes


@Timer.timeit
def parse(data: str) -> dict[int, list[list[str]]]:
    games = dict()
    for game in data.strip().split("\n"):
        game_id, subsets = game.split(":")
        games[int(re.findall(r"\d+", game_id)[0])] = [
            subset.split(",") for subset in subsets.split(";")
        ]
    return games


@Timer.timeit
def solve(data: str) -> tuple[int, int]:
    games = parse(data)
    part1 = determine_possible_games(games)
    part2 = determine_minimum_power_set_cubes(games)

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2023, 2)))
