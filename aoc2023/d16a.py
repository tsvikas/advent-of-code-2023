from aocd import data

from aoc2023.grid import Grid, Point

TEST_INPUT = r"""
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
"""[
    1:
]


class MirrorGrid(Grid):
    def beam(
        self, start: Point = Point(0, 0), direction: Point = Point(0, 1)
    ) -> set[Point]:
        """
        >>> grid = MirrorGrid.from_string(TEST_INPUT)
        >>> beam_points = grid.beam(Point(0, 0), Point(0, 1))
        >>> Point(0, 0) in beam_points
        True
        >>> Point(1, 1) in beam_points
        True
        >>> Point(5, 5) in beam_points
        True
        >>> Point(6, 6) in beam_points
        True
        """
        positions = [(start, direction)]
        visited_positions = set()
        while positions:
            position, direction = positions.pop()
            if not self.in_bounds(position):
                continue
            if (position, direction) in visited_positions:
                continue
            visited_positions.add((position, direction))
            match self[position]:
                case ".":
                    new_directions = [direction]
                case "/":
                    new_directions = [Point(y=-direction.x, x=-direction.y)]
                case "\\":
                    new_directions = [Point(y=direction.x, x=direction.y)]
                case "-":
                    if direction.y == 0:
                        new_directions = [direction]
                    else:
                        new_directions = [Point(0, 1), Point(0, -1)]
                case "|":
                    if direction.x == 0:
                        new_directions = [direction]
                    else:
                        new_directions = [Point(1, 0), Point(-1, 0)]
                case _:
                    raise ValueError(f"invalid char {self[position]}")
            positions.extend(
                [
                    (position + new_direction, new_direction)
                    for new_direction in new_directions
                ]
            )
        return {p for p, d in visited_positions}

    def beam_energy(
        self, start: Point = Point(0, 0), direction: Point = Point(0, 1)
    ) -> int:
        """
        >>> grid = MirrorGrid.from_string(TEST_INPUT)
        >>> grid.beam_energy(Point(0, 0), Point(0, 1))
        46
        >>> grid.beam_energy(Point(0, 3), Point(1, 0))
        51
        """
        return len(self.beam(start, direction))


def process_lines(lines: str) -> int:
    """
    >>> process_lines(TEST_INPUT)
    46
    """
    return MirrorGrid.from_string(lines).beam_energy()


def main() -> int:
    lines = data
    result = process_lines(lines)
    return result


if __name__ == "__main__":
    print(main())
