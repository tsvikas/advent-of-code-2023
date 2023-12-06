from aocd import data

from aoc2023.d2a import TEST_INPUTS, Balls, Game  # noqa: F401


class GameWithPower(Game):
    @property
    def power(self) -> int:
        """
        >>> [GameWithPower.from_line(line).power for line in TEST_INPUTS]
        [48, 12, 1560, 630, 36]
        """
        max_balls = self.max_balls()
        return max_balls.red * max_balls.green * max_balls.blue


def process_lines(lines: list[str]) -> int:
    """
    >>> process_lines(TEST_INPUTS)
    2286
    """
    return sum(GameWithPower.from_line(line).power for line in lines)


def main() -> int:
    lines = data.splitlines()
    result = process_lines(lines)
    return result


if __name__ == "__main__":
    print(main())
