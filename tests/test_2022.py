# Advent of Code 2022

from helpers import load_input_data


def test_day_01():
    from src.y2022.d01 import solve

    res1, res2 = solve(load_input_data(2022, 1))

    assert res1 == 71_934, f"Part1 = {res1}"
    assert res2 == 211_447, f"Part2 = {res2}"


def test_day_02():
    from src.y2022.d02 import solve

    res1, res2 = solve(load_input_data(2022, 2))

    assert res1 == 11_873, f"Part1 = {res1}"
    assert res2 == 12_014, f"Part2 = {res2}"


def test_day_03():
    from src.y2022.d03 import solve

    res1, res2 = solve(load_input_data(2022, 3))

    assert res1 == 8_515, f"Part1 = {res1}"
    assert res2 == 2_434, f"Part2 = {res2}"


def test_day_04():
    from src.y2022.d04 import solve

    res1, res2 = solve(load_input_data(2022, 4))

    assert res1 == 528, f"Part1 = {res1}"
    assert res2 == 881, f"Part2 = {res2}"


def test_day_05():
    from src.y2022.d05 import solve

    res1, res2 = solve(load_input_data(2022, 5))

    assert res1 == "QNNTGTPFN", f"Part1 = {res1}"
    assert res2 == "GGNPJBTTR", f"Part2 = {res2}"


def test_day_06():
    from src.y2022.d06 import solve

    res1, res2 = solve(load_input_data(2022, 6))

    assert res1 == 1833, f"Part1 = {res1}"
    assert res2 == 3425, f"Part2 = {res2}"


def test_day_07():
    from src.y2022.d07 import solve

    res1, res2 = solve(load_input_data(2022, 7))

    assert res1 == 1_454_188, f"Part1 = {res1}"
    assert res2 == 4_183_246, f"Part2 = {res2}"


def test_day_08():
    from src.y2022.d08 import solve

    res1, res2 = solve(load_input_data(2022, 8))

    assert res1 == 1_805, f"Part1 = {res1}"
    assert res2 == 444_528, f"Part2 = {res2}"


def test_day_09():
    from src.y2022.d09 import solve

    res1, res2 = solve(load_input_data(2022, 9))

    assert res1 == 6_197, f"Part1 = {res1}"
    assert res2 == 2_562, f"Part2 = {res2}"


def test_day_10():
    from src.y2022.d10 import solve

    res1, res2 = solve(load_input_data(2022, 10))

    assert res1 == 15_020, f"Part1 = {res1}"
    assert res2 == "EFUGLPAP", f"Part2 = {res2}"


def test_day_11():
    from src.y2022.d11 import solve

    res1, res2 = solve(load_input_data(2022, 11))

    assert res1 == 110_264, f"Part1 = {res1}"
    assert res2 == 23_612_457_316, f"Part2 = {res2}"


def test_day_12():
    from src.y2022.d12 import solve

    res1, res2 = solve(load_input_data(2022, 12))

    assert res1 == 517, f"Part1 = {res1}"
    assert res2 == 512, f"Part2 = {res2}"


def test_day_13():
    from src.y2022.d13 import solve

    res1, res2 = solve(load_input_data(2022, 13))

    assert res1 == 5_825, f"Part1 = {res1}"
    assert res2 == 24_477, f"Part2 = {res2}"


def test_day_14():
    from src.y2022.d14 import solve

    res1, res2 = solve(load_input_data(2022, 14))

    assert res1 == 843, f"Part1 = {res1}"
    assert res2 == 27_625, f"Part2 = {res2}"


def test_day_15():
    from src.y2022.d15 import solve

    res1, res2 = solve(load_input_data(2022, 15))

    assert res1 == 4_725_496, f"Part1 = {res1}"
    assert res2 == 12_051_287_042_458, f"Part2 = {res2}"


def test_day_16():
    from src.y2022.d16 import solve

    res1, res2 = solve(load_input_data(2022, 16))

    assert res1 == 1_820, f"Part1 = {res1}"
    assert res2 == 2_602, f"Part2 = {res2}"


def test_day_17():
    from src.y2022.d17 import solve

    res1, res2 = solve(load_input_data(2022, 17))

    assert res1 == 3_117, f"Part1 = {res1}"
    assert res2 == 1_553_314_121_019, f"Part2 = {res2}"


def test_day_18():
    from src.y2022.d18 import solve

    res1, res2 = solve(load_input_data(2022, 18))

    assert res1 == 3_448, f"Part1 = {res1}"
    assert res2 == 2_052, f"Part2 = {res2}"


def test_day_19():
    from src.y2022.d19 import solve

    res1, res2 = solve(load_input_data(2022, 19))

    assert res1 == 1_127, f"Part1 = {res1}"
    assert res2 == 21_546, f"Part2 = {res2}"


def test_day_20():
    from src.y2022.d20 import solve

    res1, res2 = solve(load_input_data(2022, 20))

    assert res1 == 6_712, f"Part1 = {res1}"
    assert res2 == 1_595_584_274_798, f"Part2 = {res2}"


def test_day_21():
    from src.y2022.d21 import solve

    res1, res2 = solve(load_input_data(2022, 21))

    assert res1 == 169_525_884_255_464, f"Part1 = {res1}"
    assert res2 == 3_247_317_268_284, f"Part2 = {res2}"


def test_day_22():
    from src.y2022.d22 import solve

    res1, res2 = solve(load_input_data(2022, 22))

    assert res1 == 123_046, f"Part1 = {res1}"
    assert res2 == 195_032, f"Part2 = {res2}"


def test_day_23():
    from src.y2022.d23 import solve

    res1, res2 = solve(load_input_data(2022, 23))

    assert res1 == 4_005, f"Part1 = {res1}"
    assert res2 == 1_008, f"Part2 = {res2}"


def test_day_24():
    from src.y2022.d24 import solve

    res1, res2 = solve(load_input_data(2022, 24))

    assert res1 == 322, f"Part1 = {res1}"
    assert res2 == 974, f"Part2 = {res2}"


def test_day_25():
    from src.y2022.d25 import solve

    res = solve(load_input_data(2022, 25))

    assert res == "2-0-020-1==1021=--01", f"Part1 = {res}"
