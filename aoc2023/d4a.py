from aoc2023.common import INPUTS_DIR

TEST_INPUTS = [
    "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
    "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19",
    "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1",
    "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83",
    "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36",
    "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11",
]


def score_card(line):
    """
    >>> [score_card(line) for line in TEST_INPUTS]
    [8, 2, 2, 1, 0, 0]
    """
    numbers = line.split(":")[1]
    winning_numbers = [int(s) for s in numbers.split("|")[0].split()]
    card_numbers = [int(s) for s in numbers.split("|")[1].split()]
    num_wins = sum(n in winning_numbers for n in card_numbers)
    return 0 if num_wins == 0 else 2 ** (num_wins - 1)


def process_lines(lines):
    """
    >>> process_lines(TEST_INPUTS)
    13
    """
    return sum(score_card(line) for line in lines)


def main():
    input_fn = INPUTS_DIR / "4.txt"
    lines = input_fn.read_text().splitlines()
    result = process_lines(lines)
    return result


if __name__ == "__main__":
    print(main())
