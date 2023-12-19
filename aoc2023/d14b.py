from aocd import data, submit  # type: ignore[attr-defined]

from aoc2023.d14a import (
    TEST_INPUT,  # noqa: F401
    RocksMap,
)


def cycle(rocks: RocksMap, n: int) -> RocksMap:
    """
    >>> rocks = RocksMap.from_lines(TEST_INPUT.splitlines())
    >>> print("|", cycle(rocks, 1))
    | .....#....
    ....#...O#
    ...OO##...
    .OO#......
    .....OOO#.
    .O#...O#.#
    ....O#....
    ......OOOO
    #...O###..
    #..OO#....
    >>> print("|", cycle(rocks, 2))
    | .....#....
    ....#...O#
    .....##...
    ..O#......
    .....OOO#.
    .O#...O#.#
    ....O#...O
    .......OOO
    #..OO###..
    #.OOO#...O
    >>> print("|", cycle(rocks, 3))
    | .....#....
    ....#...O#
    .....##...
    ..O#......
    .....OOO#.
    .O#...O#.#
    ....O#...O
    .......OOO
    #...O###.O
    #.OOO#...O
    """
    cache = {hash(rocks): 0}
    cycle_length = i = None
    for i in range(1, n + 1):
        rocks = rocks.tilt_north().tilt_west().tilt_south().tilt_east()
        rocks_b = hash(rocks)
        if rocks_b in cache:
            cycle_start = cache[rocks_b]
            cycle_length = i - cycle_start
            break
        cache[rocks_b] = i
    if cycle_length is not None:
        while (n - i) % cycle_length != 0:
            i += 1
            rocks = rocks.tilt_north().tilt_west().tilt_south().tilt_east()
    return rocks


def process_lines(lines: str) -> int:
    """
    >>> process_lines(TEST_INPUT)
    64
    """
    rocks = RocksMap.from_lines(lines.splitlines())
    return cycle(rocks, 1_000_000_000).total_load_north()


def main() -> int:
    return process_lines(data)


if __name__ == "__main__":
    submit(main(), part=__file__[-4])
