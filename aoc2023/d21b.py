from aoc2023.common import Solution
from aoc2023.d21a import map_to_locations, step
from aoc2023.d21a import process_lines as process_lines_a
from aoc2023.grid import Point

TEST_INPUT = """\
...........
......##...
.###..#..#.
..#.#...#..
....#.#....
.....S.....
.##......#.
.......##..
.##.#.####.
..#...#.#..
...........
"""


def expand_map(data: str, n: int) -> str:
    lines = data.splitlines()
    expanded_lines = (
        n * [line.replace("S", ".") * (2 * n + 1) for line in lines]
        + [
            line.replace("S", ".") * n + line + line.replace("S", ".") * n
            for line in lines
        ]
        + n * [line.replace("S", ".") * (2 * n + 1) for line in lines]
    )
    return "\n".join(expanded_lines)


TEST_INPUT_EXPANDED = expand_map(TEST_INPUT, 5)


def count_reachable(
    start: Point, valid_locations: set[Point], ns: list[int]
) -> list[int]:
    assert start in valid_locations
    assert ns == sorted(ns)
    last_new_locations: set[Point] = {start}
    last_old_locations: set[Point] = set()
    previous_locations: set[Point] = set()
    reachable = []
    for n in range(ns[-1]):
        if n in ns:
            reachable.append(len(last_new_locations | last_old_locations))
        last_new_locations, last_old_locations, previous_locations = step(
            last_new_locations, last_old_locations, previous_locations, valid_locations
        )
    reachable.append(len(last_new_locations | last_old_locations))
    return reachable


def solve_quadratic_series(series: list[int], k: int) -> int:
    d1, d2 = series[1] - series[0], series[2] - series[1]
    dd1 = d2 - d1
    return series[0] + d1 * k + dd1 * (k * (k - 1) // 2)


def count_infinite_reachable(lines: str, n: int) -> int:
    lines_ = lines.splitlines()
    size_y = len(lines_)
    size_x = len(lines_[0])
    assert size_y == size_x
    assert size_y % 2 == 1
    assert lines_[size_y // 2][size_x // 2] == "S"
    st = size_y // 2
    k = (n - st) // size_y
    assert n == st + k * size_y
    expanded_lines = expand_map(lines, 4)
    start, valid_locations = map_to_locations(expanded_lines)
    reachable = count_reachable(
        start, valid_locations, [st + i * size_y for i in range(3)]
    )
    return solve_quadratic_series(reachable, k)


def process_lines(lines: str, n: int = 26501365) -> int:
    return count_infinite_reachable(lines, n)


solution = Solution.from_file(
    __file__,
    process_lines,
    {
        (TEST_INPUT, 5 + 4 * 11): (
            lambda: process_lines_a(TEST_INPUT_EXPANDED, 5 + 4 * 11)
        )
    },
)

if __name__ == "__main__":
    solution.test_inputs()
    solution.submit()
