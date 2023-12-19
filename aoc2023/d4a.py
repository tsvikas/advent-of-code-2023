from dataclasses import dataclass

from aocd import data

TEST_INPUT = """\
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""


@dataclass
class Card:
    card_id: int
    winning_numbers: list[int]
    card_numbers: list[int]

    @classmethod
    def from_line(cls, line: str) -> "Card":
        card_id = int(line.split(":")[0].replace("Card ", ""))
        numbers = line.split(":")[1]
        winning_numbers = [int(s) for s in numbers.split("|")[0].split()]
        card_numbers = [int(s) for s in numbers.split("|")[1].split()]
        return cls(card_id, winning_numbers, card_numbers)

    def wins_count(self) -> int:
        """
        >>> [Card.from_line(line).wins_count() for line in TEST_INPUT.splitlines()]
        [4, 2, 2, 1, 0, 0]
        """
        return sum(n in self.winning_numbers for n in self.card_numbers)

    def score(self) -> int:
        """
        >>> [Card.from_line(line).score() for line in TEST_INPUT.splitlines()]
        [8, 2, 2, 1, 0, 0]
        """
        num_wins = self.wins_count()
        score = 0 if num_wins == 0 else int(2 ** (num_wins - 1))
        return score


def process_lines(lines: str) -> int:
    """
    >>> process_lines(TEST_INPUT)
    13
    """
    return sum(Card.from_line(line).score() for line in lines.splitlines())


def main() -> int:
    return process_lines(data)


if __name__ == "__main__":
    print(main())
