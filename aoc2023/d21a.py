from aoc2023.common import Solution
from aoc2023.grid import Point

TEST_INPUT = """\
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
"""


def map_to_locations(lines: str) -> tuple[Point, set[Point]]:
    valid_locations = set()
    start = None
    for y, line in enumerate(lines.splitlines()):
        for x, char in enumerate(line):
            if char == "S":
                start = Point(y, x)
            if char in ["S", "."]:
                valid_locations.add(Point(y, x))
    assert start is not None
    return start, valid_locations


def step(
    last_new_locations: set[Point],
    last_old_locations: set[Point],
    previous_locations: set[Point],
    valid_locations: set[Point],
) -> tuple[set[Point], set[Point], set[Point]]:
    new_locations = set()
    for location in last_new_locations:
        for new_location in [
            location.up(),
            location.down(),
            location.left(),
            location.right(),
        ]:
            if (new_location in valid_locations) and (
                new_location not in previous_locations
            ):
                new_locations.add(new_location)
    return new_locations, previous_locations, last_new_locations | last_old_locations


def steps(start: Point, valid_locations: set[Point], n: int) -> set[Point]:
    last_new_locations: set[Point] = {start}
    last_old_locations: set[Point] = set()
    previous_locations: set[Point] = set()
    for _ in range(n):
        last_new_locations, last_old_locations, previous_locations = step(
            last_new_locations, last_old_locations, previous_locations, valid_locations
        )
    return last_new_locations | last_old_locations


def count_reachable(start: Point, valid_locations: set[Point], n: int) -> int:
    assert start in valid_locations
    return len(steps(start, valid_locations, n))


def process_lines(lines: str, n: int = 64) -> int:
    start, valid_locations = map_to_locations(lines)
    return count_reachable(start, valid_locations, n)


solution = Solution.from_file(__file__, process_lines, {(TEST_INPUT, 6): 16})

if __name__ == "__main__":
    solution.test_inputs()
    solution.submit()
