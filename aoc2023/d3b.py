import collections
import re

from aocd import data

from aoc2023.d3a import TEST_INPUT  # noqa: F401


def extract_gear_ratios(engine_schematic: list[str]) -> list[int]:
    """
    >>> extract_gear_ratios(TEST_INPUT.splitlines())
    [16345, 451490]
    """
    gears = collections.defaultdict(list)
    for line_num, line in enumerate(engine_schematic):
        # find all numbers in the line
        for match in re.finditer(r"\d+", line):
            y0 = line_num
            x1, x2 = match.span()
            value = int(match.group())
            for y in range(max(0, y0 - 1), min(y0 + 2, len(engine_schematic))):
                slice_start = max(0, x1 - 1)
                slice_end = min(x2 + 1, len(engine_schematic[y]))
                line_slice = engine_schematic[y][slice_start:slice_end]
                if "*" in line_slice:
                    x = line_slice.index("*") + slice_start
                    gears[y, x].append(value)
                    break
    expected_number_of_values = 2
    gear_ratios = [
        gear_values[0] * gear_values[1]
        for location, gear_values in gears.items()
        if len(gear_values) == expected_number_of_values
    ]
    return gear_ratios


def process_lines(lines: str) -> int:
    """
    >>> process_lines(TEST_INPUT)
    467835
    """
    return sum(extract_gear_ratios(lines.splitlines()))


def main() -> int:
    return process_lines(data)


if __name__ == "__main__":
    print(main())
