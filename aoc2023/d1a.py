import re

from aoc2023.common import INPUTS_DIR

TEST_INPUTS = ["1abc2", "pqr3stu8vwx", "a1b2c3d4e5f", "treb7uchet"]


def process_line(line: str) -> int:
    """
    >>> [process_line(line) for line in TEST_INPUTS]
    [12, 38, 15, 77]
    """
    match = re.fullmatch(r"[^\d]*(\d).*(\d)[^\d]*", line)
    if match is not None:
        first_digit = int(match.group(1))
        second_digit = int(match.group(2))
    else:
        match = re.fullmatch(r"[^\d]*(\d).*", line)
        if match is None:
            raise ValueError(f"Invalid line: {line}")
        first_digit = second_digit = int(match.group(1))
    return 10 * first_digit + second_digit


def process_lines(lines: list[str]) -> int:
    """
    >>> process_lines(TEST_INPUTS)
    142
    """
    return sum(process_line(line) for line in lines)


def main() -> int:
    input_fn = INPUTS_DIR / "1.txt"
    lines = input_fn.read_text().splitlines()
    result = process_lines(lines)
    return result


if __name__ == "__main__":
    print(main())
