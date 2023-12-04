from aocd import data

from aoc2023.d2a import TEST_INPUTS, Balls, game_max_balls  # noqa: F401


def get_game_power(line: str) -> int:
    """
    >>> [get_game_power(line) for line in TEST_INPUTS]
    [48, 12, 1560, 630, 36]
    """
    _game_id_str, games_str = line.split(":")
    max_balls = game_max_balls(games_str)
    game_power = max_balls.red * max_balls.green * max_balls.blue
    return game_power


def process_lines(lines: list[str]) -> int:
    """
    >>> process_lines(TEST_INPUTS)
    2286
    """
    return sum(get_game_power(line) for line in lines)


def main() -> int:
    lines = data.splitlines()
    result = process_lines(lines)
    return result


if __name__ == "__main__":
    print(main())
