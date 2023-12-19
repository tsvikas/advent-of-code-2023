import numpy as np
from aocd import data

TEST_INPUTS = [
    "0 3 6 9 12 15",
    "1 3 6 10 15 21",
    "10 13 16 21 30 45",
]


def next_value(line: str) -> int:
    """
    >>> [next_value(line) for line in TEST_INPUTS]
    [18, 28, 68]
    """
    values = np.array([int(x) for x in line.split()])
    diffs = [values]
    while not (diffs[-1] == 0).all():
        diffs.append(np.diff(diffs[-1]))
    last_diff = 0
    for diff in reversed(diffs):
        last_diff += diff[-1]
    return last_diff


def process_lines(lines: list[str]) -> int:
    """
    >>> process_lines(TEST_INPUTS)
    114
    """
    return sum(next_value(line) for line in lines)


def main() -> int:
    return process_lines(data.splitlines())


if __name__ == "__main__":
    print(main())
