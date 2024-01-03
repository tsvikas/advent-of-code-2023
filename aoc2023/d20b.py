from aoc2023.common import Solution
from aoc2023.d20a import Modules


def process_lines(lines: str) -> int:
    return Modules.from_lines(lines).rx_low_count()


solution = Solution.from_file(__file__, process_lines, {})

if __name__ == "__main__":
    solution.test_inputs()
    solution.submit()
