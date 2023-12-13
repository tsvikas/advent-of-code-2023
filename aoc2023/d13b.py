import collections

from aocd import data

from aoc2023.d13a import TEST_INPUTS, print_mirrors, split_maps, transpose  # noqa: F401


def find_mirror_row_above(mirrors: list[str]) -> list[int]:
    """
    >>> find_mirror_row_above([".#.", "#.#", "#..", ".#."])
    [2]
    >>> find_mirror_row_above([".#.", "#.#", "#..", ".#.", ".#.", "#.."])
    [2]
    """
    pattern_lines = collections.defaultdict(list)
    for i, line in enumerate(mirrors):
        pattern_lines[line].append(i)
    # reflection from top
    total_rows_above_reflections: list[int] = []
    possible_rows = (
        set(pattern_lines[mirrors[0]])
        .union(r + 1 for r in pattern_lines[mirrors[1]])
        .difference([0, len(mirrors)])
        .union([1])
    )
    for possible_row in possible_rows:
        size_of_reflection, mod = divmod(possible_row + 1, 2)
        if mod != 0:
            continue
        smudges = 0
        for row in range(size_of_reflection):
            reflected_to = possible_row - row
            if reflected_to not in pattern_lines[mirrors[row]]:
                if (
                    smudges == 0
                    and sum(
                        c1 != c2
                        for c1, c2 in zip(
                            mirrors[row], mirrors[reflected_to], strict=True
                        )
                    )
                    == 1
                ):
                    smudges = 1
                else:
                    smudges = 0
                    break
        if smudges == 1:
            total_rows_above_reflections.append(size_of_reflection)
    return total_rows_above_reflections


def find_mirror_row(mirrors: list[str]) -> list[int]:
    return find_mirror_row_above(mirrors) + [
        len(mirrors) - r for r in find_mirror_row_above(mirrors[::-1])
    ]


def analyze_map(mirrors: list[str]) -> int:
    """
    >>> [analyze_map(mirrors) for mirrors in split_maps(TEST_INPUTS)]
    [300, 100]
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


def process_lines(lines: str) -> int:
    """
    >>> process_lines(TEST_INPUTS)
    400
    """
    return sum(analyze_map(mirrors) for mirrors in split_maps(lines))


def main() -> int:
    lines = data
    result = process_lines(lines)
    return result


if __name__ == "__main__":
    print(main())
