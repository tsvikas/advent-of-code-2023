from collections.abc import Iterable
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


def tilt_line(line: Iterable[str]) -> list[str]:
    """
    >>> ''.join(tilt_line('O....#....'))
    'O....#....'
    >>> ''.join(tilt_line('O.OO#....#'))
    'OOO.#....#'
    >>> ''.join(tilt_line('.....##...'))
    '.....##...'
    >>> ''.join(tilt_line('OO.#O....O'))
    'OO.#OO....'
    """
    new_line: list[str] = []
    new_section_rocks = 0
    new_section_spaces = 0
    for c in line:
        match c:
            case "O":
                new_section_rocks += 1
            case ".":
                new_section_spaces += 1
            case "#":
                new_line += (
                    ["O"] * new_section_rocks + ["."] * new_section_spaces + ["#"]
                )
                new_section_rocks = 0
                new_section_spaces = 0
            case _:
                raise ValueError(f"illegal character {c!r}")
    new_line += ["O"] * new_section_rocks + ["."] * new_section_spaces
    return new_line


@dataclass
class RocksMap:
    array: npt.NDArray[np.string_]

    def __hash__(self) -> int:
        return hash(self.array.tobytes())

    def __str__(self) -> str:
        return "\n".join("".join(row) for row in self.array)

    def transpose(self) -> Self:
        """
        >>> rocks = RocksMap.from_lines(TEST_INPUT.splitlines())
        >>> print(rocks.transpose())
        OO.O.O..##
        ...OO....O
        .O...#O..O
        .O.#......
        .#.O......
        #.#..O#.##
        ..#...O.#.
        ....O#.O#.
        ....#.....
        .#.O.#O...
        """
        return self.__class__(self.array.T)

    def tilt_west(self) -> Self:
        return self.__class__(np.array([tilt_line(line) for line in self.array]))

    def tilt_north(self) -> Self:
        """
        >>> rocks = RocksMap.from_lines(TEST_INPUT.splitlines())
        >>> print(rocks.tilt_north())
        OOOO.#.O..
        OO..#....#
        OO..O##..O
        O..#.OO...
        ........#.
        ..#....#.#
        ..O..#.O.O
        ..O.......
        #....###..
        #....#....
        """
        return self.transpose().tilt_west().transpose()

    def tilt_east(self) -> Self:
        return self.__class__(
            np.array([tilt_line(line[::-1])[::-1] for line in self.array])
        )

    def tilt_south(self) -> Self:
        return self.transpose().tilt_east().transpose()

    @classmethod
    def from_lines(cls, lines: list[str]) -> Self:
        return cls(np.array([list(line) for line in lines]))

    def total_load_north(self) -> int:
        """
        >>> rocks = RocksMap.from_lines(TEST_INPUT.splitlines())
        >>> rocks.tilt_north().total_load_north()
        136
        """
        return sum(
            len(column) - row
            for column in self.array.transpose()
            for row, char in enumerate(column)
            if char == "O"
        )


def process_lines(lines: list[str]) -> int:
    """
    >>> process_lines(TEST_INPUT.splitlines())
    136
    """
    return RocksMap.from_lines(lines).tilt_north().total_load_north()


def main() -> int:
    lines = data.splitlines()
    result = process_lines(lines)
    return result


if __name__ == "__main__":
    print(main())
