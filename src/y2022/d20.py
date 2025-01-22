# Advent of Code : Day 20 - Grove Positioning System
# https://adventofcode.com/2022/day/20


from helpers import Timer, load_input_data


@Timer.timeit
def decrypt(
    array: list[int],
    decryption_key: int,
    nb_rounds: int,
    indexes: list[int] = [1000, 2000, 3000],
) -> int:
    array = [decryption_key * val for val in array]
    n = len(array)
    indices = list(range(n))

    for i in indices * nb_rounds:
        indices.pop(j := indices.index(i))
        indices.insert((j + array[i]) % (n - 1), i)

    zero_pos = indices.index(array.index(0))
    return sum(array[indices[(zero_pos + index) % n]] for index in indexes)


@Timer.timeit
def parse(data: str) -> list[int]:
    return list(map(int, data.strip().split("\n")))


@Timer.timeit
def solve(data: str) -> tuple[int, int]:
    array = parse(data)
    part1 = decrypt(array, 1, 1)
    part2 = decrypt(array, 811589153, 10)

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2022, 20)))
