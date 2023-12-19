import numpy as np
from aocd import data, submit  # type: ignore[attr-defined]

from aoc2023.d9a import TEST_INPUT  # noqa: F401


def previous_value(line: str) -> int:
    """
    >>> [previous_value(line) for line in TEST_INPUT.splitlines()]
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


def process_lines(lines: str) -> int:
    """
    >>> process_lines(TEST_INPUT)
    2
    """
    return sum(previous_value(line) for line in lines.splitlines())


def main() -> int:
    return process_lines(data)


if __name__ == "__main__":
    submit(main(), part=__file__[-4])
