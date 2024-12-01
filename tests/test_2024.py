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
