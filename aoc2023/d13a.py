import collections

from aocd import data, submit  # type: ignore[attr-defined]

TEST_INPUT = """\
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""


def transpose(mirrors: list[str]) -> list[str]:
    """
    >>> transpose(["abc", "def", "ghi"])
    ['adg', 'beh', 'cfi']
    """
    return ["".join(row) for row in zip(*mirrors, strict=True)]


def find_mirror_row_above(mirrors: list[str]) -> list[int]:
    """
    >>> find_mirror_row_above(["#.#", ".#.", ".#.", "#.#", "...", "..#"])
    [2]
    """
    pattern_lines = collections.defaultdict(list)
    for i, line in enumerate(mirrors):
        pattern_lines[line].append(i)
    # reflection from top
    total_rows_above_reflections: list[int] = []
    for possible_row in pattern_lines[mirrors[0]]:
        if possible_row == 0:
            continue
        size_of_reflection, mod = divmod(possible_row + 1, 2)
        if mod != 0:
            continue
        if all(
            possible_row - i in pattern_lines[mirrors[i]]
            for i in range(size_of_reflection)
        ):
            total_rows_above_reflections.append(size_of_reflection)
    return total_rows_above_reflections


def find_mirror_row(mirrors: list[str]) -> list[int]:
    return find_mirror_row_above(mirrors) + [
        len(mirrors) - r for r in find_mirror_row_above(mirrors[::-1])
    ]


def print_mirrors(
    mirrors: list[str], mark_rows: list[int], mark_cols: list[int]
) -> None:
    for row, line in enumerate(mirrors):
        print(line, "v" if row + 1 in mark_rows else "^" if row in mark_rows else "")
    printed_cols = 0
    for col in mark_cols:
        print(" " * (col - printed_cols - 1) + "><", end="")
        printed_cols += col
    print()


def analyze_map(mirrors: list[str]) -> int:
    """
    >>> [analyze_map(mirrors) for mirrors in split_maps(TEST_INPUT)]
    [5, 400]
    """
    mirror_row = find_mirror_row(mirrors)
    mirror_col = find_mirror_row(transpose(mirrors))
    verbose = len(mirror_row) + len(mirror_col) > 1
    if verbose:
        print("Mirror row:", mirror_row)
        print("Mirror col:", mirror_col)
        print_mirrors(mirrors, mirror_row, mirror_col)
        print()
    mirror_row = [100 * v for v in mirror_row]
    return sum(mirror_row) + sum(mirror_col)


def split_maps(lines: str) -> list[list[str]]:
    """
    >>> split_maps("abc\\ndef\\n\\nghi\\njkl")
    [['abc', 'def'], ['ghi', 'jkl']]
    """
    return [s.splitlines() for s in lines.split("\n\n")]


def process_lines(lines: str) -> int:
    """
    >>> process_lines(TEST_INPUT)
    405
    """
    return sum(analyze_map(mirrors) for mirrors in split_maps(lines))


def main() -> int:
    return process_lines(data)


if __name__ == "__main__":
    submit(main(), part=__file__[-4])
