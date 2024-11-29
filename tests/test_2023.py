# Advent of Code 2023

from pathlib import Path

import pytest


@pytest.fixture(scope="module")
def data_dir() -> Path:
    return Path(__file__).parents[1] / "data" / "2023"


def test_day_01(data_dir: Path):
    from src.y2023.d01 import solve

    res1, res2 = solve(data_dir / "01.txt")

    assert res1 == 55_816, f"Part1 = {res1}"
    assert res2 == 54_980, f"Part2 = {res2}"


def test_day_02(data_dir: Path):
    from src.y2023.d02 import solve

    res1, res2 = solve(data_dir / "02.txt")

    assert res1 == 2_162, f"Part1 = {res1}"
    assert res2 == 72_513, f"Part2 = {res2}"


def test_day_03(data_dir: Path):
    from src.y2023.d03 import solve

    res1, res2 = solve(data_dir / "03.txt")

    assert res1 == 533_775, f"Part1 = {res1}"
    assert res2 == 78_236_071, f"Part2 = {res2}"


def test_day_04(data_dir: Path):
    from src.y2023.d04 import solve

    res1, res2 = solve(data_dir / "04.txt")

    assert res1 == 24_733, f"Part1 = {res1}"
    assert res2 == 5_422_730, f"Part2 = {res2}"


def test_day_05(data_dir: Path):
    from src.y2023.d05 import solve

    res1, res2 = solve(data_dir / "05.txt")

    assert res1 == 650_599_855, f"Part1 = {res1}"
    assert res2 == 1_240_035, f"Part2 = {res2}"


def test_day_06(data_dir: Path):
    from src.y2023.d06 import solve

    res1, res2 = solve(data_dir / "06.txt")

    assert res1 == 316_800, f"Part1 = {res1}"
    assert res2 == 45_647_654, f"Part2 = {res2}"


def test_day_07(data_dir: Path):
    from src.y2023.d07 import solve

    res1, res2 = solve(data_dir / "07.txt")

    assert res1 == 253_910_319, f"Part1 = {res1}"
    assert res2 == 254_083_736, f"Part2 = {res2}"


def test_day_08(data_dir: Path):
    from src.y2023.d08 import solve

    res1, res2 = solve(data_dir / "08.txt")

    assert res1 == 21_797, f"Part1 = {res1}"
    assert res2 == 23_977_527_174_353, f"Part2 = {res2}"


def test_day_09(data_dir: Path):
    from src.y2023.d09 import solve

    res1, res2 = solve(data_dir / "09.txt")

    assert res1 == 1_939_607_039, f"Part1 = {res1}"
    assert res2 == 1_041, f"Part2 = {res2}"


def test_day_10(data_dir: Path):
    from src.y2023.d10 import solve

    res1, res2 = solve(data_dir / "10.txt")

    assert res1 == 6_725, f"Part1 = {res1}"
    assert res2 == 383, f"Part2 = {res2}"


def test_day_11(data_dir: Path):
    from src.y2023.d11 import solve

    res1, res2 = solve(data_dir / "11.txt")

    assert res1 == 9_445_168, f"Part1 = {res1}"
    assert res2 == 742_305_960_572, f"Part2 = {res2}"


def test_day_12(data_dir: Path):
    from src.y2023.d12 import solve

    res1, res2 = solve(data_dir / "12.txt")

    assert res1 == 7_460, f"Part1 = {res1}"
    assert res2 == 6_720_660_274_964, f"Part2 = {res2}"


def test_day_13(data_dir: Path):
    from src.y2023.d13 import solve

    res1, res2 = solve(data_dir / "13.txt")

    assert res1 == 34_772, f"Part1 = {res1}"
    assert res2 == 35_554, f"Part2 = {res2}"


def test_day_14(data_dir: Path):
    from src.y2023.d14 import solve

    res1, res2 = solve(data_dir / "14.txt")

    assert res1 == 105_208, f"Part1 = {res1}"
    assert res2 == 102_943, f"Part2 = {res2}"


def test_day_15(data_dir: Path):
    from src.y2023.d15 import solve

    res1, res2 = solve(data_dir / "15.txt")

    assert res1 == 510_792, f"Part1 = {res1}"
    assert res2 == 269_410, f"Part2 = {res2}"


def test_day_16(data_dir: Path):
    from src.y2023.d16 import solve

    res1, res2 = solve(data_dir / "16.txt")

    assert res1 == 7_543, f"Part1 = {res1}"
    assert res2 == 8_231, f"Part2 = {res2}"


def test_day_17(data_dir: Path):
    from src.y2023.d17 import solve

    res1, res2 = solve(data_dir / "17.txt")

    assert res1 == 674, f"Part1 = {res1}"
    assert res2 == 773, f"Part2 = {res2}"


def test_day_18(data_dir: Path):
    from src.y2023.d18 import solve

    res1, res2 = solve(data_dir / "18.txt")

    assert res1 == 50_603, f"Part1 = {res1}"
    assert res2 == 96_556_251_590_677, f"Part2 = {res2}"


def test_day_19(data_dir: Path):
    from src.y2023.d19 import solve

    res1, res2 = solve(data_dir / "19.txt")

    assert res1 == 319_062, f"Part1 = {res1}"
    assert res2 == 118_638_369_682_135, f"Part2 = {res2}"


def test_day_20(data_dir: Path):
    from src.y2023.d20 import solve

    res1, res2 = solve(data_dir / "20.txt")

    assert res1 == 873_301_506, f"Part1 = {res1}"
    assert res2 == 241_823_802_412_393, f"Part2 = {res2}"


def test_day_21(data_dir: Path):
    from src.y2023.d21 import solve

    res1, res2 = solve(data_dir / "21.txt")

    assert res1 == 3_830, f"Part1 = {res1}"
    assert res2 == 637_087_163_925_555, f"Part2 = {res2}"


def test_day_22(data_dir: Path):
    from src.y2023.d22 import solve

    res1, res2 = solve(data_dir / "22.txt")

    assert res1 == 468, f"Part1 = {res1}"
    assert res2 == 75_358, f"Part2 = {res2}"


def test_day_23(data_dir: Path):
    from src.y2023.d23 import solve

    res1, res2 = solve(data_dir / "23.txt")

    assert res1 == 2_246, f"Part1 = {res1}"
    assert res2 == 6_622, f"Part2 = {res2}"


def test_day_24(data_dir: Path):
    from src.y2023.d24 import solve

    res1, res2 = solve(data_dir / "24.txt")

    assert res1 == 31_921, f"Part1 = {res1}"
    assert res2 == 761_691_907_059_631, f"Part2 = {res2}"


def test_day_25(data_dir: Path):
    from src.y2023.d25 import solve

    res = solve(data_dir / "25.txt")

    assert res == 552_695, f"Part1 = {res}"
