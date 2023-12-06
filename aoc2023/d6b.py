from aocd import data

from aoc2023.d6a import TEST_INPUT, Race  # noqa: F401


def parse_lines(lines: list[str]) -> Race:
    """
    >>> parse_lines(TEST_INPUT.splitlines())
    Race(time=71530, distance=940200)
    """
    time = int("".join(lines[0].split()[1:]))
    distance = int("".join(lines[1].split()[1:]))
    return Race(time, distance)


def process_lines(lines: list[str]) -> int:
    """
    >>> process_lines(TEST_INPUT.splitlines())
    71503
    """
    return parse_lines(lines).n_ways_to_beat()


def main() -> int:
    lines = data.splitlines()
    result = process_lines(lines)
    return result


if __name__ == "__main__":
    print(main())
