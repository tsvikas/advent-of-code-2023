import itertools
from collections.abc import Generator, Iterable

from aocd import data

TEST_INPUT = """\
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""

TEST_INPUT_EXPENDED = """\
....#........
.........#...
#............
.............
.............
........#....
.#...........
............#
.............
.............
.........#...
#....#.......
"""


def expand_grid(grid: list[str]) -> list[str]:
    """
    >>> expand_grid(TEST_INPUT.splitlines()) == TEST_INPUT_EXPENDED.splitlines()
    True
    """
    for _ in range(2):
        grid = [
            "".join(grid[j][i] for j in range(len(grid))) for i in range(len(grid[0]))
        ]
        new_grid = []
        for line in grid:
            new_grid.append(line)
            if line == "." * len(line):
                new_grid.append("." * len(line))
        grid = new_grid
    return grid


def extract_galaxies(grid: list[str]) -> Generator[tuple[int, int], None, None]:
    """
    >>> list(extract_galaxies(TEST_INPUT.splitlines()))
    [(0, 3), (1, 7), (2, 0), (4, 6), (5, 1), (6, 9), (8, 7), (9, 0), (9, 4)]
    """
    for i, line in enumerate(grid):
        for j, char in enumerate(line):
            if char == "#":
                yield i, j


def distance_galaxies(
    galaxies: Iterable[tuple[int, int]]
) -> Generator[int, None, None]:
    """
    >>> list(distance_galaxies(extract_galaxies(TEST_INPUT.splitlines())))[:5]
    [5, 5, 7, 7, 12]
    """
    for g1, g2 in itertools.combinations(galaxies, 2):
        yield abs(g1[0] - g2[0]) + abs(g1[1] - g2[1])


def distance_galaxies_on_map(lines: list[str]) -> list[int]:
    """
    >>> distance_galaxies_on_map(TEST_INPUT.splitlines())[:5]
    [6, 6, 9, 9, 15]
    """
    grid = expand_grid(lines)
    galaxies = extract_galaxies(grid)
    distances = distance_galaxies(galaxies)
    return list(distances)


def process_lines(lines: str) -> int:
    """
    >>> process_lines(TEST_INPUT)
    374
    """
    return sum(distance_galaxies_on_map(lines.splitlines()))


def main() -> int:
    return process_lines(data)


if __name__ == "__main__":
    print(main())
