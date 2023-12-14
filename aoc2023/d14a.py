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

TEST_INPUT_TILTED = """\
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


def total_load(space: list[str]) -> int:
    """
    >>> total_load(TEST_INPUT.splitlines())
    136
    """
    load = 0
    for column in zip(*space, strict=True):
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
    return total_load(lines)


def main() -> int:
    lines = data.splitlines()
    result = process_lines(lines)
    return result


if __name__ == "__main__":
    print(main())
