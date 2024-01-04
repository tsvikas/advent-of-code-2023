from aoc2023.common import Solution
from aoc2023.d2a import TEST_INPUT, Game


class GameWithPower(Game):
    @property
    def power(self) -> int:
        """
        >>> [GameWithPower.from_line(line).power for line in TEST_INPUT.splitlines()]
        [48, 12, 1560, 630, 36]
        """
        max_balls = self.max_balls()
        return max_balls.red * max_balls.green * max_balls.blue


def process_lines(lines: str) -> int:
    return sum(GameWithPower.from_line(line).power for line in lines.splitlines())


solution = Solution.from_file(__file__, process_lines, {TEST_INPUT: 2286})

if __name__ == "__main__":
    solution.test_inputs()
    solution.submit()
