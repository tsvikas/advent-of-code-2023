from aoc2023.common import Solution
from aoc2023.d4a import TEST_INPUT, Card


def get_cards_count(cards: list[Card]) -> list[int]:
    """
    >>> get_cards_count([Card.from_line(line) for line in TEST_INPUT.splitlines()])
    [1, 2, 4, 8, 14, 1]
    """
    cards_count = [1] * len(cards)
    for card_idx, card_count in enumerate(cards_count):
        num_wins = cards[card_idx].wins_count()
        for card_won in range(card_idx + 1, card_idx + num_wins + 1):
            cards_count[card_won] += card_count
    return cards_count


def process_lines(lines: str) -> int:
    return sum(get_cards_count([Card.from_line(line) for line in lines.splitlines()]))


solution = Solution.from_file(__file__, process_lines, {TEST_INPUT: 30})

if __name__ == "__main__":
    solution.test_inputs()
    solution.submit()
