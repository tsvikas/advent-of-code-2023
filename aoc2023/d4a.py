from aocd import data

TEST_INPUTS = [
    "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53",
    "Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19",
    "Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1",
    "Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83",
    "Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36",
    "Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11",
]


def card_wins_count(line: str) -> int:
    """
    >>> [card_wins_count(line) for line in TEST_INPUTS]
    [3, 2, 2, 1, 0, 0]
    """
    numbers = line.split(":")[1]
    winning_numbers = [int(s) for s in numbers.split("|")[0].split()]
    card_numbers = [int(s) for s in numbers.split("|")[1].split()]
    num_wins = sum(n in winning_numbers for n in card_numbers)
    return num_wins


def card_score(line: str) -> int:
    """
    >>> [card_score(line) for line in TEST_INPUTS]
    [8, 2, 2, 1, 0, 0]
    """
    num_wins = card_wins_count(line)
    score = 0 if num_wins == 0 else int(2 ** (num_wins - 1))
    return score


def process_lines(lines: list[str]) -> int:
    """
    >>> process_lines(TEST_INPUTS)
    13
    """
    return sum(card_score(line) for line in lines)


def main() -> int:
    lines = data.splitlines()
    result = process_lines(lines)
    return result


if __name__ == "__main__":
    print(main())
