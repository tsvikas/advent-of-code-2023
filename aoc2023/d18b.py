from dataclasses import dataclass
from typing import Self

from aocd import data, submit  # type: ignore[attr-defined]

from aoc2023.d18a import TEST_INPUT  # noqa: F401
from aoc2023.grid import Point


@dataclass
class ShapeFixed:
    locations: list[Point]

    @staticmethod
    def split_line(line: str) -> tuple[str, int]:
        """
        >>> ShapeFixed.split_line("R 6 (#70c710)")
        ('R', 461937)
        >>> ShapeFixed.split_line("_ _ (#0dc571)")
        ('D', 56407)
        >>> ShapeFixed.split_line("_ _ (#8ceee2)")
        ('L', 577262)
        >>> ShapeFixed.split_line("_ _ (#caa173)")
        ('U', 829975)
        """
        _, _, hex_section = line.split()
        hex_number = hex_section[2:-1]
        direction = {"0": "R", "1": "D", "2": "L", "3": "U"}[hex_number[-1]]
        distance = int(hex_number[:-1], 16)
        return direction, distance

    @classmethod
    def from_lines(cls, lines: list[str], *, verbose: bool = False) -> Self:
        """
        >>> _ = ShapeFixed.from_lines(TEST_INPUT.splitlines(), verbose=True)
        #70c710 = R 461937
        #0dc571 = D 56407
        #5713f0 = R 356671
        #d2c081 = D 863240
        #59c680 = R 367720
        #411b91 = D 266681
        #8ceee2 = L 577262
        #caa173 = U 829975
        #1b58a2 = L 112010
        #caa171 = D 829975
        #7807d2 = L 491645
        #a77fa3 = U 686074
        #015232 = L 5411
        #7a21e3 = U 500254
        """
        location = Point(0, 0)
        locations = []
        for line in lines:
            direction, distance = cls.split_line(line)
            if verbose:
                print(f"{line.split()[-1][1:-1]} = {direction} {distance}")
            if direction == "U":
                direction_vector = Point(-1, 0)
            elif direction == "D":
                direction_vector = Point(1, 0)
            elif direction == "L":
                direction_vector = Point(0, -1)
            elif direction == "R":
                direction_vector = Point(0, 1)
            else:
                raise ValueError(f"illegal direction {direction!r}")
            location += direction_vector * distance
            locations.append(location)
        return cls(locations)

    def get_polygon_area(self) -> int:
        interior_area2 = 0
        last_location = self.locations[-1]
        for location in self.locations:
            interior_area2 += (
                last_location.x * location.y - location.x * last_location.y
            )
            last_location = location
        return abs(interior_area2) // 2

    def get_boundry_area(self) -> int:
        boundry_area = 0
        last_location = self.locations[-1]
        for location in self.locations:
            assert last_location.x == location.x or last_location.y == location.y
            boundry_area += abs(last_location.x - location.x) + abs(
                last_location.y - location.y
            )
            last_location = location
        return boundry_area

    def get_interior_area(self) -> int:
        return self.get_polygon_area() - self.get_boundry_area() // 2 + 1

    def get_area(self) -> int:
        return self.get_interior_area() + self.get_boundry_area()


def process_lines(lines: str) -> int:
    """
    >>> process_lines(TEST_INPUT)
    952408144115
    """
    return ShapeFixed.from_lines(lines.splitlines()).get_area()


def main() -> int:
    return process_lines(data)


if __name__ == "__main__":
    submit(main(), part=__file__[-4])
