from aoc2023.common import Solution
from aoc2023.d17a import TEST_INPUT, HeatGrid

TEST_INPUT_2 = """\
111111111111
999999999991
999999999991
999999999991
999999999991
"""


def process_lines(lines: str) -> int:
    return HeatGrid.from_line(lines).least_heat_loss(4, 10)


solution = Solution.from_file(
    __file__, process_lines, {TEST_INPUT: 94, TEST_INPUT_2: 71}
)

if __name__ == "__main__":
    solution.submit()
