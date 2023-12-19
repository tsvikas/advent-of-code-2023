from aoc2023.common import Solution
from aoc2023.d12a import TEST_INPUT, count_arrangements, parse


def duplicate(record: str, damaged: tuple[int, ...]) -> tuple[str, tuple[int, ...]]:
    return "?".join([record] * 5), damaged * 5


def process_lines(lines: str) -> int:
    return sum(
        count_arrangements(*duplicate(*parse(line))) for line in lines.splitlines()
    )


solution = Solution.from_file(__file__, process_lines, {TEST_INPUT: 525152})

if __name__ == "__main__":
    solution.submit()
