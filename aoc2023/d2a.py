import re
from dataclasses import dataclass

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


def game_is_valid(line: str) -> tuple[int, bool]:
    """
    >>> [game_is_valid(line) for line in TEST_INPUTS]
    [(1, True), (2, True), (3, False), (4, False), (5, True)]
    """
    game_id_str, games_str = line.split(":")
    game_id_match = re.fullmatch(r"Game (\d+)", game_id_str)
    if game_id_match is None:
        raise ValueError(f"Invalid game ID: {game_id_str}")
    game_id = int(game_id_match.group(1))
    games = [
        Balls(
            **{
                ball_str.split()[1]: int(ball_str.split()[0])
                for ball_str in game_str.split(", ")
            }
        )
        for game_str in games_str.split(";")
    ]
    max_balls = Balls(
        red=max(g.red for g in games),
        green=max(g.green for g in games),
        blue=max(g.blue for g in games),
    )
    limit_ball = Balls(red=12, green=13, blue=14)
    is_valid_game = all(
        getattr(max_balls, ball) <= getattr(limit_ball, ball)
        for ball in ("red", "green", "blue")
    )
    return game_id, is_valid_game


def process_lines(lines: list[str]) -> int:
    """
    >>> process_lines(TEST_INPUTS)
    8
    """
    return sum(
        game_id
        for game_id, is_valid_game in (game_is_valid(line) for line in lines)
        if is_valid_game
    )


def main() -> int:
    lines = data.splitlines()
    result = process_lines(lines)
    return result


if __name__ == "__main__":
    print(main())
