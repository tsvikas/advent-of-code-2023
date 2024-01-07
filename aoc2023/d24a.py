import itertools
from dataclasses import dataclass
from typing import Self

from aoc2023.common import Solution

TEST_INPUT = """\
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
"""


@dataclass
class HailStone:
    x: int
    y: int
    z: int
    vx: int
    vy: int
    vz: int

    @classmethod
    def from_line(cls, line: str) -> Self:
        xyz, v_xyz = line.split(" @ ")
        x, y, z = map(int, xyz.split(", "))
        vx, vy, vz = map(int, v_xyz.split(", "))
        return cls(x, y, z, vx, vy, vz)

    def __repr__(self) -> str:
        return f"{self.x}, {self.y}, {self.z} @ {self.vx}, {self.vy}, {self.vz}"

    @property
    def position(self) -> tuple[int, int, int]:
        return self.x, self.y, self.z


def cross_path_xy(a: HailStone, b: HailStone) -> tuple[float, float] | None:
    """
    >>> a = HailStone(19, 13, 30, -2, 1, -2)
    >>> b = HailStone(18, 19, 22, -1, -1, -2)
    >>> cross_path_xy(a, b)
    (14.333333333333332, 15.333333333333334)
    >>> cross_path_xy(a, HailStone(12, 31, 28, -1, -2, -1))
    (6.199999999999999, 19.4)
    >>> cross_path_xy(a, HailStone(20, 19, 15, 1, -5, -3))
    >>> cross_path_xy(b, HailStone(20, 25, 34, -2, -2, -4))
    """
    # see https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection
    d = a.vx * b.vy - a.vy * b.vx
    if d == 0:
        # parallel
        return None
    t = ((b.x - a.x) * b.vy - (b.y - a.y) * b.vx) / d
    u = ((b.x - a.x) * a.vy - (b.y - a.y) * a.vx) / d
    if t < 0 or u < 0:
        # in the past
        return None
    px = a.x + t * a.vx
    py = a.y + t * a.vy
    return px, py


def is_cross_path_xy(a: HailStone, b: HailStone, min_xy: int, max_xy: int) -> bool:
    """
    >>> a = HailStone(19, 13, 30, -2, 1, -2)
    >>> b = HailStone(18, 19, 22, -1, -1, -2)
    >>> is_cross_path_xy(a, HailStone(18, 19, 22, -1, -1, -2), 7, 27)
    True
    >>> is_cross_path_xy(a, HailStone(12, 31, 28, -1, -2, -1), 7, 27)
    False
    >>> is_cross_path_xy(a, HailStone(20, 19, 15, 1, -5, -3), 7, 27)
    False
    >>> is_cross_path_xy(b, HailStone(20, 25, 34, -2, -2, -4), 7, 27)
    False
    """
    pxy = cross_path_xy(a, b)
    if pxy is None:
        return False
    px, py = pxy
    return min_xy <= px <= max_xy and min_xy <= py <= max_xy


def crossing_stones(lines: str, min_xy: int, max_xy: int) -> int:
    stones = [HailStone.from_line(line) for line in lines.splitlines()]
    return sum(
        is_cross_path_xy(a, b, min_xy, max_xy)
        for a, b in itertools.combinations(stones, 2)
    )


def process_lines(
    lines: str, min_xy: int = 200000000000000, max_xy: int = 400000000000000
) -> int:
    return crossing_stones(lines, min_xy, max_xy)


solution = Solution.from_file(__file__, process_lines, {(TEST_INPUT, 7, 27): 2})

if __name__ == "__main__":
    solution.test_inputs()
    solution.submit()
