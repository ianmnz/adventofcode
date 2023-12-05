# Advent of Code : Day 15 - Beacon Exclusion Zone
# https://adventofcode.com/2022/day/15


def merge_intervals(intervals: list) -> list:
    intervals.sort()
    stack = [intervals[0]]

    for i in intervals[1:]:
        if stack[-1][0] <= i[0] <= stack[-1][1]:
            # If interval overlap
            stack[-1] = (stack[-1][0], max(stack[-1][1], i[1]))
        else:
            stack.append(i)

    # print(stack)
    return stack


def row_coverage(row: int, sensors: list, distances: list,
                 lower_bound: int = None, upper_bound: int = None) -> tuple:
    row_coverage = []
    nb_positions_covered = 0

    for (sensor_x, sensor_y), dist in zip(sensors, distances):
        y_offset = abs(row - sensor_y)
        x_margin = dist - y_offset

        # print(f"{sensor_x=} {sensor_y=} {dist=} {y_offset=} {x_margin=}")

        if x_margin < 0:
            continue

        lower = sensor_x - x_margin
        upper = sensor_x + x_margin

        # print(lower, upper)

        if lower_bound is not None:
            lower = max(lower_bound, lower)
            upper = max(lower_bound, upper)

        if upper_bound is not None:
            lower = min(upper_bound, lower)
            upper = min(upper_bound, upper)

        # print(lower, upper)

        row_coverage.append((lower, upper))

    row_coverage = merge_intervals(row_coverage)

    for lower, upper in row_coverage:
        nb_positions_covered += upper - lower + 1

    return row_coverage, nb_positions_covered


def main():
    sensors = []
    beacons = []
    distances = []

    lower_bound, upper_bound = 0, 4000000
    freq_constant = 4000000
    distress_beacons_freq = []

    row_of_interest = 2000000
    beacons_on_row_of_interest = set()
    nb_covered_positions_on_row_of_interest = 0

    with open('input.txt', 'r') as file:
        for line in file:
            line = line.strip().split()

            sensor_x = int(line[2].rstrip(',').lstrip('x='))
            sensor_y = int(line[3].rstrip(':').lstrip('y='))

            beacon_x = int(line[8].rstrip(',').lstrip('x='))
            beacon_y = int(line[9].lstrip('y='))

            dist = abs(beacon_x - sensor_x) + abs(beacon_y - sensor_y)

            if beacon_y == row_of_interest:
                beacons_on_row_of_interest.add(beacon_y)

            sensors.append((sensor_x, sensor_y))
            beacons.append((beacon_x, beacon_y))
            distances.append(dist)

    _, row_of_interest_coverage = row_coverage(row_of_interest, sensors, distances)

    # print(row_of_interest_coverage)
    # print(len(beacons_on_row_of_interest))

    nb_covered_positions_on_row_of_interest = row_of_interest_coverage - len(beacons_on_row_of_interest)

    # Answer part 1 :
    print(f"Nb of positions that cannot contain a beacon on row y="
          f"{row_of_interest}: {nb_covered_positions_on_row_of_interest}") # 4725496


    # --- Part II ---
    for y in range(lower_bound, upper_bound + 1):
        coverage, nb_positions_covered = row_coverage(y, sensors, distances, lower_bound, upper_bound)

        # print(row, coverage, nb_positions_covered)

        if nb_positions_covered == (upper_bound - lower_bound + 1):
            # Covers all the row
            continue

        x = lower_bound
        while lower_bound <= x <= upper_bound:
            for lower, upper in coverage:
                if x > upper:
                    continue

                elif lower <= x <= upper:
                    x = upper + 1
                    continue

                else:
                    distress_beacon_freq = x * freq_constant + y
                    distress_beacons_freq.append((x, y, distress_beacon_freq))
                    x += 1
                    # print(f"({x=}, {y=}) => {distress_beacon_freq}")
                    break

    # # Answer part 2 :
    print(f"Tuning frequency of distress beacon" # x = 3012821, y = 3042458
          f": {distress_beacons_freq}") # 12051287042458

if __name__ == "__main__":
    main()