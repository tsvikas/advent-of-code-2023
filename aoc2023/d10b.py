import numpy as np

from aoc2023.common import Solution
from aoc2023.d10a import (
    Point,
    get_next_direction,
    get_start_direction,
    get_start_location,
)

TEST_INPUT_1 = """\
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
"""
TEST_INPUT_2 = """\
..........
.S------7.
.|F----7|.
.||OOOO||.
.||OOOO||.
.|L-7F-J|.
.|II||II|.
.L--JL--J.
..........
"""

TEST_INPUT_3 = """\
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
"""

TEST_INPUT_4 = """\
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
"""


def is_counterclockwise(direction: Point, next_direction: Point) -> bool:
    return (direction.x * next_direction.y - direction.y * next_direction.x) > 0


def find_enclosed(lines: list[str]) -> int:
    """
    >>> find_enclosed(TEST_INPUT_1.splitlines())
    4
    >>> find_enclosed(TEST_INPUT_2.splitlines())
    4
    >>> find_enclosed(TEST_INPUT_3.splitlines())
    8
    >>> find_enclosed(TEST_INPUT_4.splitlines())
    10
    """
    location = start_location = get_start_location(lines)
    direction = start_direction = get_start_direction(lines, start_location)
    turns = np.zeros(shape=(len(lines), len(lines[0])), dtype=int)
    part_of_loop = np.zeros(shape=(len(lines), len(lines[0])), dtype=bool)
    while True:
        next_location = location + direction
        part_of_loop[next_location.y, next_location.x] = True
        if next_location != start_location:
            next_pipe = lines[next_location.y][next_location.x]
            try:
                next_direction = get_next_direction(next_pipe, direction)
            except ValueError as e:
                raise ValueError(f"disconnected loop at {next_location}") from e
        else:
            next_direction = start_direction
        if next_direction != direction:
            fill_below = next_direction.y > 0 or direction.y < 0
            fill_right = next_direction.x > 0 or direction.x < 0
            ccw = is_counterclockwise(direction, next_direction)
            below_right_sign = 1 if (ccw == (fill_below == fill_right)) else -1
            turns[next_location.y :, next_location.x :] += below_right_sign
            turns[: next_location.y, : next_location.x] += below_right_sign
            turns[next_location.y :, : next_location.x] += -below_right_sign
            turns[: next_location.y :, next_location.x :] += -below_right_sign
        if next_location == start_location:
            break
        location = next_location
        direction = next_direction
    turns = turns * ~part_of_loop
    assert ((turns % 4) == 0).all()
    full_turns = abs(turns // 4)
    inner_locations: int = full_turns.sum()
    return inner_locations


def process_lines(lines: str) -> int:
    return find_enclosed(lines.splitlines())


solution = Solution.from_file(
    __file__,
    process_lines,
    {TEST_INPUT_1: 4, TEST_INPUT_2: 4, TEST_INPUT_3: 8, TEST_INPUT_4: 10},
)

if __name__ == "__main__":
    solution.submit()
