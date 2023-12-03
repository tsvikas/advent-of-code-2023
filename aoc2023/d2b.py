import re
from pathlib import Path

from aoc2023.d2a import (
    TEST_INPUTS,  # noqa: F401
    Balls,
)


def process_line(line):
    """
    >>> [process_line(line) for line in TEST_INPUTS]
    [(1, 48), (2, 12), (3, 1560), (4, 630), (5, 36)]
    """
    game_id_str, games_str = line.split(":")
    game_id = int(re.fullmatch(r"Game (\d+)", game_id_str).group(1))
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
    game_power = max_balls.red * max_balls.green * max_balls.blue
    return game_id, game_power


def process_lines(lines):
    """
    >>> process_lines(TEST_INPUTS)
    2286
    """
    game_results = dict(process_line(line) for line in lines)
    return sum(game_power for game_id, game_power in game_results.items())


def main():
    input_fn = Path("../inputs") / "2.txt"
    lines = input_fn.read_text().splitlines()
    result = process_lines(lines)
    print(result)


if __name__ == "__main__":
    main()
