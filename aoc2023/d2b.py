from aocd import data

from aoc2023.d2a import TEST_INPUTS, Balls  # noqa: F401


def process_line(line: str) -> int:
    """
    >>> [process_line(line) for line in TEST_INPUTS]
    [48, 12, 1560, 630, 36]
    """
    _game_id_str, games_str = line.split(":")
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
    return game_power


def process_lines(lines: list[str]) -> int:
    """
    >>> process_lines(TEST_INPUTS)
    2286
    """
    return sum(process_line(line) for line in lines)


def main() -> int:
    lines = data.splitlines()
    result = process_lines(lines)
    return result


if __name__ == "__main__":
    print(main())
