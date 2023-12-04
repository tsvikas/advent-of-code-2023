from aoc2023.common import INPUTS_DIR
from aoc2023.d4a import TEST_INPUTS  # noqa: F401


def score_card(line: str) -> int:
    """
    >>> [score_card(line) for line in TEST_INPUTS]
    [4, 2, 2, 1, 0, 0]
    """
    numbers = line.split(":")[1]
    winning_numbers = [int(s) for s in numbers.split("|")[0].split()]
    card_numbers = [int(s) for s in numbers.split("|")[1].split()]
    num_wins = sum(n in winning_numbers for n in card_numbers)
    return num_wins


def process_cards(lines: list[str]) -> int:
    """
    >>> process_cards(TEST_INPUTS)
    30
    """
    cards_count = {i: 1 for i in range(len(lines))}
    for card_idx, card_count in cards_count.items():
        card = lines[card_idx]
        num_wins = score_card(card)
        for winned_card in range(card_idx + 1, card_idx + num_wins + 1):
            cards_count[winned_card] += card_count

    return sum(cards_count.values())


def main() -> int:
    input_fn = INPUTS_DIR / "4.txt"
    lines = input_fn.read_text().splitlines()
    result = process_cards(lines)
    return result


if __name__ == "__main__":
    print(main())
