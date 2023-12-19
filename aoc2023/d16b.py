from aocd import data, submit  # type: ignore[attr-defined]
from joblib.parallel import Parallel, delayed  # type: ignore[import-untyped]

from aoc2023.d16a import TEST_INPUT, MirrorGrid  # noqa: F401
from aoc2023.grid import Point


def max_energized(line: str) -> int:
    """
    >>> max_energized(TEST_INPUT)
    51
    """
    mirrors = MirrorGrid.from_string(line)
    max_y, max_x = mirrors.data.shape
    init_positions = (
        [(Point(y, 0), Point(0, 1)) for y in range(max_y)]
        + [(Point(0, x), Point(1, 0)) for x in range(max_x)]
        + [(Point(y, max_x - 1), Point(0, -1)) for y in range(max_y)]
        + [(Point(max_y - 1, x), Point(-1, 0)) for x in range(max_x)]
    )
    beam_energies: list[int] = Parallel(n_jobs=-1, verbose=0)(
        delayed(mirrors.beam_energy)(*init_position) for init_position in init_positions
    )
    return max(beam_energies)


def process_lines(lines: str) -> int:
    """
    >>> process_lines(TEST_INPUT)
    51
    """
    return max_energized(lines)


def main() -> int:
    return process_lines(data)


if __name__ == "__main__":
    submit(main(), part=__file__[-4])
