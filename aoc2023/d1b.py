import re

from aocd import data

TEST_INPUTS = [
    "two1nine",
    "eightwothree",
    "abcone2threexyz",
    "xtwone3four",
    "4nineeightseven2",
    "zoneight234",
    "7pqrstsixteen",
]
DIGITS = {
    # zero was not included in the requirements
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def get_digits(line: str) -> int:
    """
    >>> [get_digits(line) for line in TEST_INPUTS]
    [29, 83, 13, 24, 42, 14, 76]
    """
    digits = "|".join(DIGITS.keys())
    match = re.fullmatch(r".*?(\d|" + digits + r").*(\d|" + digits + ").*?", line)
    if match is not None:
        first_digit = match.group(1)
        first_digit = int(DIGITS.get(first_digit, first_digit))
        second_digit = match.group(2)
        second_digit = int(DIGITS.get(second_digit, second_digit))
    else:
        match = re.fullmatch(r".*(\d|" + digits + ").*", line)
        if match is None:
            raise ValueError(f"Invalid line: {line}")
        digit = match.group(1)
        digit = int(DIGITS.get(digit, digit))
        first_digit = second_digit = digit
    return 10 * first_digit + second_digit


def process_lines(lines: list[str]) -> int:
    """
    >>> process_lines(TEST_INPUTS)
    281
    """
    return sum(get_digits(line) for line in lines)


def main() -> int:
    return process_lines(data.splitlines())


if __name__ == "__main__":
    print(main())
