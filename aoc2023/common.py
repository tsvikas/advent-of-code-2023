from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Self

from aocd import get_data, submit  # type: ignore[attr-defined]

SolveInput = str | tuple[Any, ...]
SolveFunc = Callable[[Any], int]


@dataclass
class Solution:
    year: int
    day: int
    part: str
    process_lines: SolveFunc
    tests: dict[SolveInput, int]

    @classmethod
    def from_file(
        cls,
        filename: str,
        process_lines: SolveFunc,
        tests: dict[SolveInput, int],
    ) -> Self:
        year = int(filename.split("/")[-2][-4:])
        day = int(filename.split("/")[-1].split(".")[0][1:-1])
        part = filename.split("/")[-1].split(".")[0][-1]
        return cls(year, day, part, process_lines, tests)

    def test_inputs(self) -> None:
        for i, (test, expected) in enumerate(self.tests.items()):
            if isinstance(test, tuple):
                actual = self.process_lines(*test)
            else:
                actual = self.process_lines(test)
            assert actual == expected, f"{i}: {actual=} {expected=}"

    def solve(self) -> int:
        return self.process_lines(get_data(day=self.day, year=self.year))

    def submit(self) -> None:
        submit(self.solve(), part=self.part, day=self.day, year=self.year)
