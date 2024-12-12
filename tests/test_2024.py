# Advent of Code 2024

from helpers import load_input_data


def test_day_01():
    from src.y2024.d01 import solve

    res1, res2 = solve(load_input_data(2024, 1))

    assert res1 == 1_579_939, f"Part1 = {res1}"
    assert res2 == 20_351_745, f"Part2 = {res2}"


def test_day_02():
    from src.y2024.d02 import solve

    res1, res2 = solve(load_input_data(2024, 2))

    assert res1 == 390, f"Part1 = {res1}"
    assert res2 == 439, f"Part2 = {res2}"


def test_day_03():
    from src.y2024.d03 import solve

    res1, res2 = solve(load_input_data(2024, 3))

    assert res1 == 183_788_984, f"Part1 = {res1}"
    assert res2 == 62_098_619, f"Part2 = {res2}"


def test_day_04():
    from src.y2024.d04 import solve

    res1, res2 = solve(load_input_data(2024, 4))

    assert res1 == 2_358, f"Part1 = {res1}"
    assert res2 == 1_737, f"Part2 = {res2}"


def test_day_05():
    from src.y2024.d05 import solve

    res1, res2 = solve(load_input_data(2024, 5))

    assert res1 == 5_129, f"Part1 = {res1}"
    assert res2 == 4_077, f"Part2 = {res2}"


def test_day_06():
    from src.y2024.d06 import solve

    res1, res2 = solve(load_input_data(2024, 6))

    assert res1 == 4_988, f"Part1 = {res1}"
    assert res2 == 1_697, f"Part2 = {res2}"


def test_day_07():
    from src.y2024.d07 import solve

    res1, res2 = solve(load_input_data(2024, 7))

    assert res1 == 2_437_272_016_585, f"Part1 = {res1}"
    assert res2 == 162_987_117_690_649, f"Part2 = {res2}"


def test_day_08():
    from src.y2024.d08 import solve

    res1, res2 = solve(load_input_data(2024, 8))

    assert res1 == 392, f"Part1 = {res1}"
    assert res2 == 1_235, f"Part2 = {res2}"


def test_day_09():
    from src.y2024.d09 import solve

    res1, res2 = solve(load_input_data(2024, 9))

    assert res1 == 6_341_711_060_162, f"Part1 = {res1}"
    assert res2 == 6_377_400_869_326, f"Part2 = {res2}"


def test_day_10():
    from src.y2024.d10 import solve

    res1, res2 = solve(load_input_data(2024, 10))

    assert res1 == 737, f"Part1 = {res1}"
    assert res2 == 1_619, f"Part2 = {res2}"


def test_day_11():
    from src.y2024.d11 import solve

    res1, res2 = solve(load_input_data(2024, 11))

    assert res1 == 224_529, f"Part1 = {res1}"
    assert res2 == 266_820_198_587_914, f"Part2 = {res2}"


def test_day_12():
    from y2024.d12 import solve

    res1, res2 = solve(load_input_data(2024, 12))

    assert res1 == 1_359_028, f"Part1 = {res1}"
    assert res2 == 839_780, f"Part2 = {res2}"
