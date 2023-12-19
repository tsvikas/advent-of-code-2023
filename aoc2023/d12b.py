from aocd import data

from aoc2023.d12a import TEST_INPUT, count_arrangements, parse  # noqa: F401


def duplicate(record: str, damaged: tuple[int, ...]) -> tuple[str, tuple[int, ...]]:
    return "?".join([record] * 5), damaged * 5


def process_lines(lines: str) -> int:
    """
    >>> process_lines(TEST_INPUT)
    525152
    """
    return sum(
        count_arrangements(*duplicate(*parse(line))) for line in lines.splitlines()
    )


def main() -> int:
    return process_lines(data)


if __name__ == "__main__":
    print(main())
