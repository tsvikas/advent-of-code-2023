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


def step(start_locations: set[Point], valid_locations: set[Point]) -> set[Point]:
    end_locations = set()
    for location in start_locations:
        for new_location in [
            location.up(),
            location.down(),
            location.left(),
            location.right(),
        ]:
            if new_location in valid_locations:
                end_locations.add(new_location)
    return end_locations


def steps(start: Point, valid_locations: set[Point], n: int) -> set[Point]:
    locations = {start}
    for _ in range(n):
        locations = step(locations, valid_locations)
    return locations


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
