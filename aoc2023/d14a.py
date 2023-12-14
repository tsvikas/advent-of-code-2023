from dataclasses import dataclass
from typing import Self

import numpy as np
import numpy.typing as npt
from aocd import data

TEST_INPUT = """\
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""


@dataclass
class RocksMap:
    array: npt.NDArray[np.string_]

    def __str__(self) -> str:
        return "\n".join("".join(row) for row in self.array)

    @classmethod
    def from_lines(cls, lines: list[str]) -> Self:
        return cls(np.array([list(line) for line in lines]))

    def total_load_north(self) -> int:
        """
        >>> rocks = RocksMap.from_lines(TEST_INPUT.splitlines())
        >>> rocks.total_load_north()
        136
        """
        load = 0
        for column in self.array.transpose():
            next_load = len(column)
            for row, char in enumerate(column):
                match char:
                    case "#":
                        next_load = len(column) - 1 - row
                    case "O":
                        load += next_load
                        next_load -= 1
                    case ".":
                        pass
                    case _:
                        raise ValueError(f"illegal character: {char}")
        return load


def process_lines(lines: list[str]) -> int:
    """
    >>> process_lines(TEST_INPUT.splitlines())
    136
    """
    return RocksMap.from_lines(lines).total_load_north()


def main() -> int:
    lines = data.splitlines()
    result = process_lines(lines)
    return result


if __name__ == "__main__":
    print(main())
