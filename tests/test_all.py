import importlib
import tomllib
from pathlib import Path
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from aoc2023.common import Solution

SOLUTIONS = tomllib.loads(
    Path(__file__).parent.joinpath("my_solutions.toml").read_text()
)


@pytest.mark.parametrize(("name", "expected"), list(SOLUTIONS.items()))
def test_all(name: str, expected: int):
    module = importlib.import_module(f"aoc2023.{name}")
    solution: Solution = module.solution
    solution.test_inputs()
    assert solution.solve() == expected
