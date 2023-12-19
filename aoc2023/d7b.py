import collections

from aocd import data

from aoc2023.d7a import TEST_INPUT, Hand, HandType, get_winning  # noqa: F401


class HandWithJoker(Hand):
    def card_rank(self, card: str) -> int:
        return {"T": 10, "J": 1, "Q": 12, "K": 13, "A": 14}.get(card) or int(card)

    @property
    def hand_type(self) -> HandType:
        joker_count = self.cards.count("J")
        if joker_count == 5:  # noqa: PLR2004
            return HandType.FIVE_OF_A_KIND
        card_count = collections.Counter(self.cards.replace("J", ""))
        count_1st, *count_rest = (count for _card, count in card_count.most_common(2))
        count_1st += joker_count
        count_2nd = count_rest[0] if count_rest else 0
        match (count_1st, count_2nd):
            case [5, 0]:
                return HandType.FIVE_OF_A_KIND
            case [4, 1]:
                return HandType.FOUR_OF_A_KIND
            case [3, 2]:
                return HandType.FULL_HOUSE
            case [3, 1]:
                return HandType.THREE_OF_A_KIND
            case [2, 2]:
                return HandType.TWO_PAIR
            case [2, 1]:
                return HandType.ONE_PAIR
            case [1, 1]:
                return HandType.HIGH_CARD
            case _:
                raise ValueError(f"Invalid card count: {card_count}")


def process_lines(lines: str) -> int:
    """
    >>> process_lines(TEST_INPUT)
    5905
    """
    return sum(
        get_winning(HandWithJoker.from_line(line) for line in lines.splitlines())
    )


def main() -> int:
    return process_lines(data)


if __name__ == "__main__":
    print(main())
