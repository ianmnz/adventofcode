# Advent of Code 2024

from pathlib import Path

import pytest


@pytest.fixture(scope="module")
def data_dir() -> Path:
    return Path(__file__).parents[1] / "data" / "2024"


def test_day_01(data_dir: Path):
    from src.y2024.d01 import solve

    res1, res2 = solve(data_dir / "01.txt")

    assert res1 == 1_579_939, f"Part1 = {res1}"
    assert res2 == 20_351_745, f"Part2 = {res2}"


def test_day_02(data_dir):
    from src.y2024.d02 import solve

    res1, res2 = solve(data_dir / "02.txt")

    assert res1 == 390, f"Part1 = {res1}"
    assert res2 == 439, f"Part2 = {res2}"


def test_day_03(data_dir):
    from src.y2024.d03 import solve

    res1, res2 = solve(data_dir / "03.txt")

    assert res1 == 183_788_984, f"Part1 = {res1}"
    assert res2 == 62_098_619, f"Part2 = {res2}"


def test_day_04(data_dir):
    from src.y2024.d04 import solve

    res1, res2 = solve(data_dir / "04.txt")

    assert res1 == 2_358, f"Part1 = {res1}"
    assert res2 == 1_737, f"Part2 = {res2}"
