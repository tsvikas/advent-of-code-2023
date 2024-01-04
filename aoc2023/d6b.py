from aoc2023.common import Solution
from aoc2023.d6a import TEST_INPUT, Race


def parse_lines(lines: list[str]) -> Race:
    """
    >>> parse_lines(TEST_INPUT.splitlines())
    Race(time=71530, distance=940200)
    """
    time = int("".join(lines[0].split()[1:]))
    distance = int("".join(lines[1].split()[1:]))
    return Race(time, distance)


def process_lines(lines: str) -> int:
    return parse_lines(lines.splitlines()).n_ways_to_beat()


solution = Solution.from_file(__file__, process_lines, {TEST_INPUT: 71503})

if __name__ == "__main__":
    solution.test_inputs()
    solution.submit()
