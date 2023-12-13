import collections

from aocd import data

TEST_INPUTS = """\
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


def find_mirror_row(mirrors: list[str]) -> list[int]:
    """
    >>> find_mirror_row(["#.#", ".#.", ".#.", "#.#", "...", "..#"])
    [2]
    >>> find_mirror_row(["...", "..#", "#.#", ".#.", ".#.", ".#.", ".#.", "#.#"])
    [5]
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
    # reflection from bottom
    for possible_row in pattern_lines[mirrors[-1]]:
        if possible_row == len(mirrors) - 1:
            continue
        size_of_reflection, mod = divmod(len(mirrors) - possible_row, 2)
        if mod != 0:
            continue
        if all(
            possible_row + i in pattern_lines[mirrors[len(mirrors) - 1 - i]]
            for i in range(size_of_reflection)
        ):
            total_rows_above_reflections.append(len(mirrors) - size_of_reflection)
    return total_rows_above_reflections


def analyze_map(mirrors: list[str]) -> int:
    """
    >>> [analyze_map(mirrors) for mirrors in split_maps(TEST_INPUTS)]
    [5, 400]
    """
    mirror_row = find_mirror_row(mirrors)
    mirror_col = find_mirror_row(transpose(mirrors))
    verbose = len(mirror_row) + len(mirror_col) > 1
    if verbose:
        print("Mirror row:", mirror_row)
        print("Mirror col:", mirror_col)
        for row, line in enumerate(mirrors):
            print(
                line, "v" if row + 1 in mirror_row else "^" if row in mirror_row else ""
            )
        cumcol = 1
        for col in mirror_col:
            print(" " * (col - cumcol) + "><", end="")
            cumcol += col
        print()
        print()
    mirror_row = [100 * v for v in mirror_row]
    return sum(mirror_row) + sum(mirror_col)


def split_maps(lines: str) -> list[list[str]]:
    r"""
    >>> split_maps("abc\ndef\n\nghi\njkl")
    [['abc', 'def'], ['ghi', 'jkl']]
    """
    return [s.splitlines() for s in lines.split("\n\n")]


def process_lines(lines: str) -> int:
    """
    >>> process_lines(TEST_INPUTS)
    405
    """
    return sum(analyze_map(mirrors) for mirrors in split_maps(lines))


def main() -> int:
    lines = data
    result = process_lines(lines)
    return result


if __name__ == "__main__":
    print(main())
