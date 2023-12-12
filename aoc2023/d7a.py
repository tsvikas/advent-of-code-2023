import collections
from collections.abc import Iterable
from dataclasses import dataclass
from enum import IntEnum
from typing import Self

from aocd import data

TEST_INPUTS = [
    "32T3K 765",
    "T55J5 684",
    "KK677 28",
    "KTJJT 220",
    "QQQJA 483",
]


class HandType(IntEnum):
    FIVE_OF_A_KIND = 6
    FOUR_OF_A_KIND = 5
    FULL_HOUSE = 4
    THREE_OF_A_KIND = 3
    TWO_PAIR = 2
    ONE_PAIR = 1
    HIGH_CARD = 0


@dataclass
class Hand:
    cards: str
    bid: int

    def card_rank(self, card: str) -> int:
        return {"T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}.get(card) or int(card)

    @property
    def card_values(self) -> list[int]:
        return [self.card_rank(card) for card in self.cards]

    @property
    def hand_type(self) -> HandType:
        card_count = collections.Counter(self.cards)
        match card_count.most_common(2):
            case [(_, 5)]:
                return HandType.FIVE_OF_A_KIND
            case [(_, 4), (_, 1)]:
                return HandType.FOUR_OF_A_KIND
            case [(_, 3), (_, 2)]:
                return HandType.FULL_HOUSE
            case [(_, 3), (_, 1)]:
                return HandType.THREE_OF_A_KIND
            case [(_, 2), (_, 2)]:
                return HandType.TWO_PAIR
            case [(_, 2), (_, 1)]:
                return HandType.ONE_PAIR
            case [(_, 1), (_, 1)]:
                return HandType.HIGH_CARD
            case _:
                raise ValueError(f"Invalid card count: {card_count}")

    @classmethod
    def from_line(cls, line: str) -> Self:
        cards, bid_str = line.split()
        return cls(cards, int(bid_str))


def get_winning(hands: Iterable[Hand]) -> list[int]:
    """
    >>> get_winning([Hand.from_line(line) for line in TEST_INPUTS])
    [765, 440, 84, 2736, 2415]
    """
    hands = sorted(hands, key=lambda hand: (hand.hand_type, hand.card_values))
    return [i * hand.bid for i, hand in enumerate(hands, 1)]


def process_lines(lines: list[str]) -> int:
    """
    >>> process_lines(TEST_INPUTS)
    6440
    """
    return sum(get_winning(Hand.from_line(line) for line in lines))


def main() -> int:
    lines = data.splitlines()
    result = process_lines(lines)
    return result


if __name__ == "__main__":
    print(main())
