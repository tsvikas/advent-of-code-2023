import itertools
from collections.abc import Generator, Iterable

from aocd import data, submit  # type: ignore[attr-defined]

from aoc2023.d11a import TEST_INPUT, extract_galaxies  # noqa: F401


def find_empty_rows_and_cols(grid: list[str]) -> tuple[list[int], list[int]]:
    """
    >>> find_empty_rows_and_cols(TEST_INPUT.splitlines())
    ([3, 7], [2, 5, 8])
    """
    empty_rows = [i for i, line in enumerate(grid) if line == "." * len(line)]
    empty_cols = [
        i for i in range(len(grid[0])) if all(line[i] == "." for line in grid)
    ]
    return empty_rows, empty_cols


def distance_galaxies(
    galaxies: Iterable[tuple[int, int]],
    empty_rows: list[int] | None = None,
    empty_cols: list[int] | None = None,
    expansion_factor: int = 1,
) -> Generator[int, None, None]:
    """
    >>> galaxies = list(extract_galaxies(TEST_INPUT.splitlines()))
    >>> empty_rows, empty_cols = find_empty_rows_and_cols(TEST_INPUT.splitlines())
    >>> list(distance_galaxies(galaxies))[:5]
    [5, 5, 7, 7, 12]
    >>> list(distance_galaxies(galaxies, empty_rows, empty_cols, 2))[:5]
    [6, 6, 9, 9, 15]
    >>> list(distance_galaxies(galaxies, empty_rows, empty_cols, 10))[:5]
    [14, 14, 25, 25, 39]
    """
    empty_rows = empty_rows or []
    empty_cols = empty_cols or []

    for g1, g2 in itertools.combinations(galaxies, 2):
        dist = abs(g1[0] - g2[0]) + abs(g1[1] - g2[1])
        empty_rows_in_between = [
            i for i in empty_rows if min(g1[0], g2[0]) < i < max(g1[0], g2[0])
        ]
        empty_cols_in_between = [
            i for i in empty_cols if min(g1[1], g2[1]) < i < max(g1[1], g2[1])
        ]
        dist_expanded = dist + (
            len(empty_rows_in_between) + len(empty_cols_in_between)
        ) * (expansion_factor - 1)
        yield dist_expanded


def distance_galaxies_on_map(lines: list[str], expansion_factor: int) -> list[int]:
    """
    >>> distance_galaxies_on_map(TEST_INPUT.splitlines(), 10)[:5]
    [14, 14, 25, 25, 39]
    """
    empty_rows, empty_cols = find_empty_rows_and_cols(lines)
    galaxies = extract_galaxies(lines)
    distances = distance_galaxies(
        galaxies, empty_rows, empty_cols, expansion_factor=expansion_factor
    )
    return list(distances)


def process_lines(lines: str, expansion_factor: int = 1000000) -> int:
    """
    >>> process_lines(TEST_INPUT, 2)
    374
    >>> process_lines(TEST_INPUT, 10)
    1030
    >>> process_lines(TEST_INPUT, 100)
    8410
    """
    return sum(distance_galaxies_on_map(lines.splitlines(), expansion_factor))


def main() -> int:
    return process_lines(data)


if __name__ == "__main__":
    submit(main(), part=__file__[-4])
