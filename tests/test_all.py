import importlib
import tomllib
from pathlib import Path

import pytest

SOLUTIONS = tomllib.loads(
    Path(__file__).parent.joinpath("my_solutions.toml").read_text()
)


@pytest.mark.parametrize(("name", "expected"), list(SOLUTIONS.items()))
def test_all(name: str, expected: int):
    module = importlib.import_module(f"aoc2023.{name}")
    assert module.solution.solve() == expected
