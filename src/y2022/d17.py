# Advent of Code : Day 17 - Pyroclastic Flow
# https://adventofcode.com/2022/day/17


from helpers import Timer, load_input_data

rocks = (
    (0, 1, 2, 3),  # - shape
    (1j, 1, 1 + 1j, 1 + 2j, 2 + 1j),  # + shape
    (0, 1, 2, 2 + 1j, 2 + 2j),  # L shape
    (0, 1j, 2j, 3j),  # I shape
    (0, 1, 1j, 1 + 1j),  # cube shape
)

rock_tops = (0, 2, 2, 3, 1)
nb_rocks = len(rocks)


RIGHT = 1
LEFT = -1
DOWN = -1j


@Timer.timeit
def simulate_fall(n: int, jets: list[int]) -> int:
    tower = set()
    cache = dict()

    def is_empty(z: complex) -> bool:
        return z.real in range(7) and z.imag > 0 and z not in tower

    def check_move(z: complex, jet: complex, rock) -> bool:
        return all(is_empty(z + jet + r) for r in rock)

    i, j, top = 0, 0, 0
    nb_jets = len(jets)

    for step in range(n):
        pos = complex(2, top + 4)

        # Cycle detection
        key = i, j
        if key in cache:
            c_step, c_top = cache[key]  # cached step, cached top
            q, r = divmod(n - step, step - c_step)
            if r == 0:
                return int(top + q * (top - c_top))
        else:
            cache[key] = step, top

        rock = rocks[i]

        while True:
            jet = jets[j]
            j = (j + 1) % nb_jets

            if check_move(pos, jet, rock):
                pos += jet  # Move sideways from jet

            if check_move(pos, DOWN, rock):
                pos += DOWN  # Fall

            else:
                break

        tower |= {pos + r for r in rock}
        top = max(top, pos.imag + rock_tops[i])
        i = (i + 1) % nb_rocks

    return int(top)


@Timer.timeit
def parse(data: str) -> list[int]:
    return [RIGHT if jet == ">" else LEFT for jet in data.strip()]


@Timer.timeit
def solve(data: str) -> tuple[int, int]:
    jets = parse(data)
    part1 = simulate_fall(2022, jets)
    part2 = simulate_fall(1_000_000_000_000, jets)

    return part1, part2


if __name__ == "__main__":
    print(solve(load_input_data(2022, 17)))
