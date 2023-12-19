import numpy as np

from aoc2023.common import Solution
from aoc2023.d9a import TEST_INPUT


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
    return sum(previous_value(line) for line in lines.splitlines())


solution = Solution.from_file(__file__, process_lines, {TEST_INPUT: 2})

if __name__ == "__main__":
    solution.submit()
