from dataclasses import dataclass

from aocd import data

TEST_INPUT_1 = """\
.....
.S-7.
.|.|.
.L-J.
.....
"""
TEST_INPUT_2 = """\
..F7.
.FJ|.
SJ.L7
|F--J
LJ...
"""


@dataclass(frozen=True)
class Point:
    y: int
    x: int

    def __add__(self, other: "Point") -> "Point":
        return Point(self.y + other.y, self.x + other.x)


def get_start_location(lines: list[str]) -> Point:
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "S":
                return Point(y, x)
    raise ValueError("No start location found")


def get_start_direction(lines: list[str], start_location: Point) -> Point:
    if lines[start_location.y][start_location.x + 1] in ["-", "J", "7"]:
        return Point(0, 1)
    if lines[start_location.y][start_location.x - 1] in ["-", "L", "F"]:
        return Point(0, -1)
    if lines[start_location.y - 1][start_location.x] in ["|", "F", "7"]:
        return Point(-1, 0)
    if lines[start_location.y + 1][start_location.x] in ["|", "J", "L"]:
        return Point(1, 0)
    raise ValueError("No direction found")


def get_next_direction(next_pipe: str, direction: Point) -> Point:
    if (next_pipe == "-" and direction in [Point(0, 1), Point(0, -1)]) or (
        next_pipe == "|" and direction in [Point(1, 0), Point(-1, 0)]
    ):
        return direction
    if next_pipe == "F" and direction in [Point(-1, 0), Point(0, -1)]:
        return direction + Point(1, 1)
    if next_pipe == "J" and direction in [Point(1, 0), Point(0, 1)]:
        return direction + Point(-1, -1)
    if next_pipe == "L" and direction in [Point(1, 0), Point(0, -1)]:
        return direction + Point(-1, 1)
    if next_pipe == "7" and direction in [Point(-1, 0), Point(0, 1)]:
        return direction + Point(1, -1)
    raise ValueError("No next direction found")


def find_farthest(lines: list[str]) -> int:
    """
    >>> find_farthest(TEST_INPUT_1.splitlines())
    4
    >>> find_farthest(TEST_INPUT_2.splitlines())
    8
    """
    location = start_location = get_start_location(lines)
    direction = get_start_direction(lines, start_location)
    loop_size = 1
    while (next_location := location + direction) != start_location:
        loop_size += 1
        next_pipe = lines[next_location.y][next_location.x]
        try:
            next_direction = get_next_direction(next_pipe, direction)
        except ValueError as e:
            raise ValueError(f"disconnected loop at {next_location}") from e
        location = next_location
        direction = next_direction
    max_distance = loop_size // 2
    return max_distance


def process_lines(lines: str) -> int:
    """
    >>> process_lines(TEST_INPUT_1)
    4
    >>> process_lines(TEST_INPUT_2)
    8
    """
    return find_farthest(lines.splitlines())


def main() -> int:
    return process_lines(data)


if __name__ == "__main__":
    print(main())
