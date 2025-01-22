# Advent of Code 2023

from helpers import load_input_data


def test_day_01():
    from src.y2023.d01 import solve

    res1, res2 = solve(load_input_data(2023, 1))

    assert res1 == 55_816, f"Part1 = {res1}"
    assert res2 == 54_980, f"Part2 = {res2}"


def test_day_02():
    from src.y2023.d02 import solve

    res1, res2 = solve(load_input_data(2023, 2))

    assert res1 == 2_162, f"Part1 = {res1}"
    assert res2 == 72_513, f"Part2 = {res2}"


def test_day_03():
    from src.y2023.d03 import solve

    res1, res2 = solve(load_input_data(2023, 3))

    assert res1 == 533_775, f"Part1 = {res1}"
    assert res2 == 78_236_071, f"Part2 = {res2}"


def test_day_04():
    from src.y2023.d04 import solve

    res1, res2 = solve(load_input_data(2023, 4))

    assert res1 == 24_733, f"Part1 = {res1}"
    assert res2 == 5_422_730, f"Part2 = {res2}"


def test_day_05():
    from src.y2023.d05 import solve

    res1, res2 = solve(load_input_data(2023, 5))

    assert res1 == 650_599_855, f"Part1 = {res1}"
    assert res2 == 1_240_035, f"Part2 = {res2}"


def test_day_06():
    from src.y2023.d06 import solve

    res1, res2 = solve(load_input_data(2023, 6))

    assert res1 == 316_800, f"Part1 = {res1}"
    assert res2 == 45_647_654, f"Part2 = {res2}"


def test_day_07():
    from src.y2023.d07 import solve

    res1, res2 = solve(load_input_data(2023, 7))

    assert res1 == 253_910_319, f"Part1 = {res1}"
    assert res2 == 254_083_736, f"Part2 = {res2}"


def test_day_08():
    from src.y2023.d08 import solve

    res1, res2 = solve(load_input_data(2023, 8))

    assert res1 == 21_797, f"Part1 = {res1}"
    assert res2 == 23_977_527_174_353, f"Part2 = {res2}"


def test_day_09():
    from src.y2023.d09 import solve

    res1, res2 = solve(load_input_data(2023, 9))

    assert res1 == 1_939_607_039, f"Part1 = {res1}"
    assert res2 == 1_041, f"Part2 = {res2}"


def test_day_10():
    from src.y2023.d10 import solve

    res1, res2 = solve(load_input_data(2023, 10))

    assert res1 == 6_725, f"Part1 = {res1}"
    assert res2 == 383, f"Part2 = {res2}"


def test_day_11():
    from src.y2023.d11 import solve

    res1, res2 = solve(load_input_data(2023, 11))

    assert res1 == 9_445_168, f"Part1 = {res1}"
    assert res2 == 742_305_960_572, f"Part2 = {res2}"


def test_day_12():
    from src.y2023.d12 import solve

    res1, res2 = solve(load_input_data(2023, 12))

    assert res1 == 7_460, f"Part1 = {res1}"
    assert res2 == 6_720_660_274_964, f"Part2 = {res2}"


def test_day_13():
    from src.y2023.d13 import solve

    res1, res2 = solve(load_input_data(2023, 13))

    assert res1 == 34_772, f"Part1 = {res1}"
    assert res2 == 35_554, f"Part2 = {res2}"


def test_day_14():
    from src.y2023.d14 import solve

    res1, res2 = solve(load_input_data(2023, 14))

    assert res1 == 105_208, f"Part1 = {res1}"
    assert res2 == 102_943, f"Part2 = {res2}"


def test_day_15():
    from src.y2023.d15 import solve

    res1, res2 = solve(load_input_data(2023, 15))

    assert res1 == 510_792, f"Part1 = {res1}"
    assert res2 == 269_410, f"Part2 = {res2}"


def test_day_16():
    from src.y2023.d16 import solve

    res1, res2 = solve(load_input_data(2023, 16))

    assert res1 == 7_543, f"Part1 = {res1}"
    assert res2 == 8_231, f"Part2 = {res2}"


def test_day_17():
    from src.y2023.d17 import solve

    res1, res2 = solve(load_input_data(2023, 17))

    assert res1 == 674, f"Part1 = {res1}"
    assert res2 == 773, f"Part2 = {res2}"


def test_day_18():
    from src.y2023.d18 import solve

    res1, res2 = solve(load_input_data(2023, 18))

    assert res1 == 50_603, f"Part1 = {res1}"
    assert res2 == 96_556_251_590_677, f"Part2 = {res2}"


def test_day_19():
    from src.y2023.d19 import solve

    res1, res2 = solve(load_input_data(2023, 19))

    assert res1 == 319_062, f"Part1 = {res1}"
    assert res2 == 118_638_369_682_135, f"Part2 = {res2}"


def test_day_20():
    from src.y2023.d20 import solve

    res1, res2 = solve(load_input_data(2023, 20))

    assert res1 == 873_301_506, f"Part1 = {res1}"
    assert res2 == 241_823_802_412_393, f"Part2 = {res2}"


def test_day_21():
    from src.y2023.d21 import solve

    res1, res2 = solve(load_input_data(2023, 21))

    assert res1 == 3_830, f"Part1 = {res1}"
    assert res2 == 637_087_163_925_555, f"Part2 = {res2}"


def test_day_22():
    from src.y2023.d22 import solve

    res1, res2 = solve(load_input_data(2023, 22))

    assert res1 == 468, f"Part1 = {res1}"
    assert res2 == 75_358, f"Part2 = {res2}"


def test_day_23():
    from src.y2023.d23 import solve

    res1, res2 = solve(load_input_data(2023, 23))

    assert res1 == 2_246, f"Part1 = {res1}"
    assert res2 == 6_622, f"Part2 = {res2}"


def test_day_24():
    from src.y2023.d24 import solve

    res1, res2 = solve(load_input_data(2023, 24))

    assert res1 == 31_921, f"Part1 = {res1}"
    assert res2 == 761_691_907_059_631, f"Part2 = {res2}"


def test_day_25():
    from src.y2023.d25 import solve

    res = solve(load_input_data(2023, 25))

    assert res == 552_695, f"Part1 = {res}"
