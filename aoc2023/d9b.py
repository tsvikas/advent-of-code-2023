import numpy as np
from aocd import data

from aoc2023.d9a import TEST_INPUTS  # noqa: F401


def previous_value(line: str) -> int:
    """
    >>> [previous_value(line) for line in TEST_INPUTS]
    [-3, 0, 5]
    """
    values = np.array([int(x) for x in line.split()])
    diffs = [values]
    while not (diffs[-1] == 0).all():
        diffs.append(np.diff(diffs[-1]))
    last_diff = 0
    for diff in reversed(diffs):
        last_diff = diff[0] - last_diff
    return last_diff


def process_lines(lines: list[str]) -> int:
    """
    >>> process_lines(TEST_INPUTS)
    2
    """
    return sum(previous_value(line) for line in lines)


def main() -> int:
    return process_lines(data.splitlines())


if __name__ == "__main__":
    print(main())
