import re

from aoc2023.common import INPUTS_DIR

TEST_INPUT = """\
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""


def adjacent_area(engine_schematic: list[str], y: int, x1: int, x2: int):
    return [
        line0[max(0, x1 - 1) : x2 + 1]
        for line0 in engine_schematic[max(0, y - 1) : y + 2]
    ]


def contains_part(area: list[str]):
    return bool(set("".join(area)) - set("0123456789."))


def extract_part_numbers(engine_schematic: list[str]):
    """
    >>> extract_part_numbers(TEST_INPUT.splitlines())
    [467, 35, 633, 617, 592, 755, 664, 598]
    """
    part_numbers = [
        int(match.group())
        for line_num, line in enumerate(engine_schematic)
        for match in re.finditer(r"\d+", line)
        if contains_part(
            adjacent_area(engine_schematic, line_num, match.start(), match.end())
        )
    ]
    return part_numbers


def process_lines(lines):
    """
    >>> process_lines(TEST_INPUT.splitlines())
    4361
    """
    return sum(extract_part_numbers(lines))


def main():
    input_fn = INPUTS_DIR / "3.txt"
    lines = input_fn.read_text().splitlines()
    result = process_lines(lines)
    return result


if __name__ == "__main__":
    print(main())
