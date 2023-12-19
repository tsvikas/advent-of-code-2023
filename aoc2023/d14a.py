from dataclasses import dataclass
from typing import Self

from aocd import data, submit  # type: ignore[attr-defined]

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


def tilt_line(line: str) -> str:
    """
    >>> tilt_line('O....#....')
    'O....#....'
    >>> tilt_line('O.OO#....#')
    'OOO.#....#'
    >>> tilt_line('.....##...')
    '.....##...'
    >>> tilt_line('OO.#O....O')
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
    return "".join(new_line)


@dataclass
class RocksMap:
    array: list[str]

    def __hash__(self) -> int:
        return hash("".join(self.array))

    def __str__(self) -> str:
        return "\n".join(self.array)

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
        return self.__class__(["".join(line) for line in zip(*self.array, strict=True)])

    def tilt_west(self) -> Self:
        """
        >>> rocks = RocksMap.from_lines(TEST_INPUT.splitlines())
        >>> print(rocks.tilt_west())
        O....#....
        OOO.#....#
        .....##...
        OO.#OO....
        OO......#.
        O.#O...#.#
        O....#OO..
        O.........
        #....###..
        #OO..#....
        """
        return self.__class__([tilt_line(line) for line in self.array])

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
        """
        >>> rocks = RocksMap.from_lines(TEST_INPUT.splitlines())
        >>> print("|", rocks.tilt_east())
        | ....O#....
        .OOO#....#
        .....##...
        .OO#....OO
        ......OO#.
        .O#...O#.#
        ....O#..OO
        .........O
        #....###..
        #..OO#....
        """
        return self.__class__([tilt_line(line[::-1])[::-1] for line in self.array])

    def tilt_south(self) -> Self:
        return self.transpose().tilt_east().transpose()

    @classmethod
    def from_lines(cls, lines: list[str]) -> Self:
        return cls(lines)

    def total_load_north(self) -> int:
        """
        >>> rocks = RocksMap.from_lines(TEST_INPUT.splitlines())
        >>> rocks.tilt_north().total_load_north()
        136
        """
        return sum(
            len(column) - row
            for column in self.transpose().array
            for row, char in enumerate(column)
            if char == "O"
        )


def process_lines(lines: str) -> int:
    """
    >>> process_lines(TEST_INPUT)
    136
    """
    return RocksMap.from_lines(lines.splitlines()).tilt_north().total_load_north()


def main() -> int:
    return process_lines(data)


if __name__ == "__main__":
    submit(main(), part=__file__[-4])
