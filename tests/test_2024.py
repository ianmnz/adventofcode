# Advent of Code 2024

from helpers import load_input_data


def test_day_01():
    from y2024.d01 import solve

    res1, res2 = solve(load_input_data(2024, 1))

    assert res1 == 1_579_939, f"Part1 = {res1}"
    assert res2 == 20_351_745, f"Part2 = {res2}"


def test_day_02():
    from y2024.d02 import solve

    res1, res2 = solve(load_input_data(2024, 2))

    assert res1 == 390, f"Part1 = {res1}"
    assert res2 == 439, f"Part2 = {res2}"


def test_day_03():
    from y2024.d03 import solve

    res1, res2 = solve(load_input_data(2024, 3))

    assert res1 == 183_788_984, f"Part1 = {res1}"
    assert res2 == 62_098_619, f"Part2 = {res2}"


def test_day_04():
    from y2024.d04 import solve

    res1, res2 = solve(load_input_data(2024, 4))

    assert res1 == 2_358, f"Part1 = {res1}"
    assert res2 == 1_737, f"Part2 = {res2}"


def test_day_05():
    from y2024.d05 import solve

    res1, res2 = solve(load_input_data(2024, 5))

    assert res1 == 5_129, f"Part1 = {res1}"
    assert res2 == 4_077, f"Part2 = {res2}"


def test_day_06():
    from y2024.d06 import solve

    res1, res2 = solve(load_input_data(2024, 6))

    assert res1 == 4_988, f"Part1 = {res1}"
    assert res2 == 1_697, f"Part2 = {res2}"


def test_day_07():
    from y2024.d07 import solve

    res1, res2 = solve(load_input_data(2024, 7))

    assert res1 == 2_437_272_016_585, f"Part1 = {res1}"
    assert res2 == 162_987_117_690_649, f"Part2 = {res2}"


def test_day_08():
    from y2024.d08 import solve

    res1, res2 = solve(load_input_data(2024, 8))

    assert res1 == 392, f"Part1 = {res1}"
    assert res2 == 1_235, f"Part2 = {res2}"


def test_day_09():
    from y2024.d09 import solve

    res1, res2 = solve(load_input_data(2024, 9))

    assert res1 == 6_341_711_060_162, f"Part1 = {res1}"
    assert res2 == 6_377_400_869_326, f"Part2 = {res2}"


def test_day_10():
    from y2024.d10 import solve

    res1, res2 = solve(load_input_data(2024, 10))

    assert res1 == 737, f"Part1 = {res1}"
    assert res2 == 1_619, f"Part2 = {res2}"


def test_day_11():
    from y2024.d11 import solve

    res1, res2 = solve(load_input_data(2024, 11))

    assert res1 == 224_529, f"Part1 = {res1}"
    assert res2 == 266_820_198_587_914, f"Part2 = {res2}"


def test_day_12():
    from y2024.d12 import solve

    res1, res2 = solve(load_input_data(2024, 12))

    assert res1 == 1_359_028, f"Part1 = {res1}"
    assert res2 == 839_780, f"Part2 = {res2}"


def test_day_13():
    from y2024.d13 import solve

    res1, res2 = solve(load_input_data(2024, 13))

    assert res1 == 35_082, f"Part1 = {res1}"
    assert res2 == 82_570_698_600_470, f"Part2 = {res2}"


def test_day_14():
    from y2024.d14 import solve

    res1, res2 = solve(load_input_data(2024, 14))

    assert res1 == 228_457_125, f"Part1 = {res1}"
    assert res2 == 6_493, f"Part2 = {res2}"


def test_day_15():
    from y2024.d15 import solve

    res1, res2 = solve(load_input_data(2024, 15))

    assert res1 == 1_406_628, f"Part1 = {res1}"
    assert res2 == 1_432_781, f"Part2 = {res2}"


def test_day_16():
    from y2024.d16 import solve

    res1, res2 = solve(load_input_data(2024, 16))

    assert res1 == 98_520, f"Part1 = {res1}"
    assert res2 == 609, f"Part2 = {res2}"


def test_day_17():
    from y2024.d17 import solve

    res1, res2 = solve(load_input_data(2024, 17))

    assert res1 == "6,0,6,3,0,2,3,1,6", f"Part1 = {res1}"
    assert res2 == 236_539_226_447_469, f"Part2 = {res2}"


def test_day_18():
    from y2024.d18 import solve

    res1, res2 = solve(load_input_data(2024, 18))

    assert res1 == 370, f"Part1 = {res1}"
    assert res2 == "65,6", f"Part2 = {res2}"


def test_day_19():
    from y2024.d19 import solve

    res1, res2 = solve(load_input_data(2024, 19))

    assert res1 == 290, f"Part1 = {res1}"
    assert res2 == 712_058_625_427_487, f"Part2 = {res2}"


def test_day_20():
    from y2024.d20 import solve

    res1, res2 = solve(load_input_data(2024, 20))

    assert res1 == 1_378, f"Part1 = {res1}"
    assert res2 == 975_379, f"Part2 = {res2}"


def test_day_21():
    from y2024.d21 import solve

    res1, res2 = solve(load_input_data(2024, 21))

    assert res1 == 125_742, f"Part1 = {res1}"
    assert res2 == 157_055_032_722_640, f"Part2 = {res2}"
