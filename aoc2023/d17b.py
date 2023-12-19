from aocd import data

from aoc2023.d17a import TEST_INPUT, HeatGrid  # noqa: F401

TEST_INPUT_2 = """\
111111111111
999999999991
999999999991
999999999991
999999999991
"""


def process_lines(lines: str) -> int:
    """
    >>> process_lines(TEST_INPUT)
    94
    >>> process_lines(TEST_INPUT_2)
    71
    """
    return HeatGrid.from_line(lines).least_heat_loss(4, 10)


def main() -> int:
    return process_lines(data)


if __name__ == "__main__":
    print(main())
