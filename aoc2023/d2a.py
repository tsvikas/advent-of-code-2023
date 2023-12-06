from dataclasses import dataclass
from typing import Self

from aocd import data

TEST_INPUTS = [
    "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green",
    "Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue",
    "Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red",
    "Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red",
    "Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green",
]


@dataclass(frozen=True)
class Balls:
    red: int = 0
    green: int = 0
    blue: int = 0

    @classmethod
    def from_string(cls, s: str) -> "Balls":
        return cls(
            **{
                ball_str.split()[1]: int(ball_str.split()[0])
                for ball_str in s.split(", ")
            }
        )


@dataclass
class Game:
    game_id: int
    draws: list[Balls]

    @classmethod
    def from_line(cls, line: str) -> Self:
        game_id_str, games_str = line.split(":")
        game_id = int(game_id_str.replace("Game ", ""))
        draws = [Balls.from_string(draw) for draw in games_str.split(";")]
        return cls(game_id, draws)

    def max_balls(self) -> Balls:
        """
        >>> Game.from_line(TEST_INPUTS[0]).max_balls()
        Balls(red=4, green=2, blue=6)
        >>> Game.from_line(TEST_INPUTS[1]).max_balls()
        Balls(red=1, green=3, blue=4)
        >>> Game.from_line(TEST_INPUTS[2]).max_balls()
        Balls(red=20, green=13, blue=6)
        >>> Game.from_line(TEST_INPUTS[3]).max_balls()
        Balls(red=14, green=3, blue=15)
        >>> Game.from_line(TEST_INPUTS[4]).max_balls()
        Balls(red=6, green=3, blue=2)
        """
        return Balls(
            red=max(draw.red for draw in self.draws),
            green=max(draw.green for draw in self.draws),
            blue=max(draw.blue for draw in self.draws),
        )

    def is_valid(self) -> bool:
        """
        >>> [Game.from_line(line).is_valid() for line in TEST_INPUTS]
        [True, True, False, False, True]
        """
        max_balls = self.max_balls()
        limit_ball = Balls(red=12, green=13, blue=14)
        is_valid_game = all(
            getattr(max_balls, ball) <= getattr(limit_ball, ball)
            for ball in ("red", "green", "blue")
        )
        return is_valid_game


def process_lines(lines: list[str]) -> int:
    """
    >>> process_lines(TEST_INPUTS)
    8
    """
    return sum(
        game.game_id for line in lines if (game := Game.from_line(line)).is_valid()
    )


def main() -> int:
    lines = data.splitlines()
    result = process_lines(lines)
    return result


if __name__ == "__main__":
    print(main())
