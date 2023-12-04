import importlib

import pytest

SOLUTIONS = {
    "d1a": 56397,
    "d1b": 55701,
    "d2a": 2505,
    "d2b": 70265,
    "d3a": 536202,
    "d3b": 78272573,
    "d4a": 27454,
    "d4b": 6857330,
}


@pytest.mark.parametrize(("name", "expected"), list(SOLUTIONS.items()))
def test_all(name: str, expected: int):
    module = importlib.import_module(f"aoc2023.{name}")
    assert module.main() == expected
