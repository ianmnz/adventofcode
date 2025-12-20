# Advent of Code 2025

from helpers import load_input_data


def test_day_01():
    from y2025.d01 import solve

    res1, res2 = solve(load_input_data(2025, 1))

    assert res1 == 962, f"Part1 = {res1}"
    assert res2 == 5782, f"Part2 = {res2}"


def test_day_02():
    from y2025.d02 import solve

    res1, res2 = solve(load_input_data(2025, 2))

    assert res1 == 18_893_502_033, f"Part1 = {res1}"
    assert res2 == 26_202_168_557, f"Part2 = {res2}"


def test_day_03():
    from y2025.d03 import solve

    res1, res2 = solve(load_input_data(2025, 3))

    assert res1 == 16_887, f"Part1 = {res1}"
    assert res2 == 167_302_518_850_275, f"Part2 = {res2}"


def test_day_04():
    from y2025.d04 import solve

    res1, res2 = solve(load_input_data(2025, 4))

    assert res1 == 1_502, f"Part1 = {res1}"
    assert res2 == 9_083, f"Part2 = {res2}"


def test_day_05():
    from y2025.d05 import solve

    res1, res2 = solve(load_input_data(2025, 5))

    assert res1 == 720, f"Part1 = {res1}"
    assert res2 == 357_608_232_770_687, f"Part2 = {res2}"


def test_day_06():
    from y2025.d06 import solve

    res1, res2 = solve(load_input_data(2025, 6))

    assert res1 == 8_108_520_669_952, f"Part1 = {res1}"
    assert res2 == 11_708_563_470_209, f"Part2 = {res2}"


def test_day_07():
    from y2025.d07 import solve

    res1, res2 = solve(load_input_data(2025, 7))

    assert res1 == 1_555, f"Part1 = {res1}"
    assert res2 == 12_895_232_295_789, f"Part2 = {res2}"


def test_day_08():
    from y2025.d08 import solve

    res1, res2 = solve(load_input_data(2025, 8))

    assert res1 == 131_580, f"Part1 = {res1}"
    assert res2 == 6_844_224, f"Part2 = {res2}"


def test_day_09():
    from y2025.d09 import solve

    res1, res2 = solve(load_input_data(2025, 9))

    assert res1 == 4_756_718_172, f"Part1 = {res1}"
    assert res2 == 1_665_679_194, f"Part2 = {res2}"


def test_day_10():
    from y2025.d10 import solve

    res1, res2 = solve(load_input_data(2025, 10))

    assert res1 == 524, f"Part1 = {res1}"
    assert res2 == 21_696, f"Part2 = {res2}"


def test_day_11():
    from y2025.d11 import solve

    res1, res2 = solve(load_input_data(2025, 11))

    assert res1 == 643, f"Part1 = {res1}"
    assert res2 == 417_190_406_827_152, f"Part2 = {res2}"


def test_day_12():
    from y2025.d12 import solve

    res1 = solve(load_input_data(2025, 12))

    assert res1 == 589, f"Part1 = {res1}"
