from dataclasses import dataclass
from typing import Self

from aocd import data

from aoc2023.grid import Point

TEST_INPUT = """\
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""


@dataclass
class Shape:
    locations: dict[Point, str]

    @classmethod
    def from_lines(cls, lines: list[str]) -> Self:
        location = Point(0, 0)
        locations = {}
        last_direction = lines[-1].split()[0]
        for line in lines:
            direction, distance_s, _color = line.split()
            distance = int(distance_s)
            locations[location] = {
                ("U", "L"): "7",
                ("U", "R"): "F",
                ("D", "L"): "J",
                ("D", "R"): "L",
                ("L", "U"): "L",
                ("L", "D"): "F",
                ("R", "U"): "J",
                ("R", "D"): "7",
            }[last_direction, direction]
            if direction == "U":
                direction_vector = Point(-1, 0)
                direction_symbol = "|"
            elif direction == "D":
                direction_vector = Point(1, 0)
                direction_symbol = "|"
            elif direction == "L":
                direction_vector = Point(0, -1)
                direction_symbol = "-"
            elif direction == "R":
                direction_vector = Point(0, 1)
                direction_symbol = "-"
            else:
                raise ValueError(f"illegal direction {direction!r}")

            for _i in range(1, distance):
                location += direction_vector
                locations[location] = direction_symbol
            location += direction_vector
            last_direction = direction
        return cls(locations)

    @property
    def min_x(self) -> int:
        return min(location.x for location in self.locations)

    @property
    def max_x(self) -> int:
        return max(location.x for location in self.locations)

    @property
    def min_y(self) -> int:
        return min(location.y for location in self.locations)

    @property
    def max_y(self) -> int:
        return max(location.y for location in self.locations)

    def __str__(self) -> str:
        return "\n".join(
            "".join(
                self.locations.get(Point(y, x), ".")
                for x in range(self.min_x, self.max_x + 1)
            )
            for y in range(self.min_y, self.max_y + 1)
        )

    def get_area(self) -> int:
        area = 0
        for y in range(self.min_y, self.max_y + 1):
            counting_f7 = False
            counting_lj = False
            counting_pipe = False
            for x in range(self.min_x, self.max_x + 1):
                if counting_f7 and counting_lj:
                    counting_f7 = False
                    counting_lj = False
                    counting_pipe = not counting_pipe
                counting = counting_lj or counting_f7 or counting_pipe
                char = self.locations.get(Point(y, x), "x" if counting else ".")
                match char:
                    case "." | "x":
                        if counting:
                            area += 1
                    case "|":
                        area += 1
                        counting_pipe = not counting_pipe
                    case "F" | "7":
                        area += 1
                        counting_f7 = not counting_f7
                    case "L" | "J":
                        area += 1
                        counting_lj = not counting_lj
                    case "-":
                        area += 1
                    case _:
                        raise ValueError(f"illegal char {char!r}")
        return area


def process_lines(lines: list[str]) -> int:
    """
    >>> process_lines(TEST_INPUT.splitlines())
    62
    """
    return Shape.from_lines(lines).get_area()


def main() -> int:
    lines = data.splitlines()
    result = process_lines(lines)
    return result


if __name__ == "__main__":
    print(main())
