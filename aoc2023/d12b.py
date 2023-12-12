from aocd import data

from aoc2023.d12a import TEST_INPUTS, count_arrangement, parse  # noqa: F401


def duplicate(record: str, damaged: tuple[int, ...]) -> tuple[str, tuple[int, ...]]:
    return "?".join([record] * 5), damaged * 5


def process_lines(lines: list[str]) -> int:
    """
    >>> process_lines(TEST_INPUTS)
    525152
    """
    return sum(count_arrangement(*duplicate(*parse(line))) for line in lines)


def main() -> int:
    lines = data.splitlines()
    result = process_lines(lines)
    return result


if __name__ == "__main__":
    print(main())
