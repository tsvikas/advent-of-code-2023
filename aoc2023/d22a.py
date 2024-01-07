import math
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Self

import numpy as np

from aoc2023.common import Solution

TEST_INPUT = """\
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
"""


@dataclass
class Point3D:
    x: int
    y: int
    z: int

    def __str__(self) -> str:
        return f"{self.x},{self.y},{self.z}"

    def __iter__(self) -> Iterator[int]:
        return iter((self.x, self.y, self.z))


@dataclass
class Brick:
    end1: Point3D
    end2: Point3D

    @classmethod
    def from_line(cls, line: str) -> Self:
        end1_s, end2_s = line.split("~")
        end1_i = tuple(map(int, end1_s.split(",")))
        end2_i = tuple(map(int, end2_s.split(",")))
        assert all(a <= b for a, b in zip(end1_i, end2_i, strict=False))
        return cls(Point3D(*end1_i), Point3D(*end2_i))

    def __repr__(self) -> str:
        return f"{self.end1}~{self.end2}"

    @property
    def size(self) -> int:
        """
        >>> Brick(Point3D(0, 0, 0), Point3D(0, 0, 0)).size
        1
        >>> Brick(Point3D(0, 0, 0), Point3D(0, 0, 1)).size
        2
        >>> Brick(Point3D(0, 0, 0), Point3D(0, 1, 1)).size
        4
        >>> Brick(Point3D(0, 0, 0), Point3D(1, 1, 1)).size
        8
        """
        return math.prod(
            abs(a - b) + 1 for a, b in zip(self.end1, self.end2, strict=False)
        )

    def to_area(self) -> tuple[slice, slice]:
        return slice(self.end1.x, self.end2.x + 1), slice(self.end1.y, self.end2.y + 1)


def drop_bricks(bricks: list[Brick]) -> tuple[dict[int, Brick], dict[int, set[int]]]:
    bricks = sorted(bricks, key=lambda brick: min(brick.end1.z, brick.end2.z))
    max_x = max(max(brick.end2.x + 1, brick.end1.x + 1) for brick in bricks)
    max_y = max(max(brick.end2.y + 1, brick.end1.y + 1) for brick in bricks)
    h_grid = np.zeros(shape=(max_x, max_y), dtype=int)
    b_grid = np.zeros(shape=(max_x, max_y), dtype=int)
    falled_bricks = {}
    supported_by = {}
    for b, brick in enumerate(bricks, 1):
        area = brick.to_area()
        max_h = h_grid[area].max()
        supported_by[b] = set(b_grid[area][h_grid[area] == max_h])
        dz = brick.end1.z - (max_h + 1)
        new_brick = Brick(
            Point3D(brick.end1.x, brick.end1.y, brick.end1.z - dz),
            Point3D(brick.end2.x, brick.end2.y, brick.end2.z - dz),
        )
        falled_bricks[b] = new_brick
        h_grid[area] = new_brick.end2.z
        b_grid[area] = b
    return falled_bricks, supported_by


def safe_to_disintegrate(supported_by: dict[int, set[int]]) -> set[int]:
    safe_bricks = set(supported_by)
    for bricks in supported_by.values():
        if len(bricks) == 1:
            brick_id = next(iter(bricks))
            if brick_id in safe_bricks:
                safe_bricks.remove(brick_id)
    return safe_bricks


def process_lines(lines: str) -> int:
    bricks = [Brick.from_line(line) for line in lines.splitlines()]
    falled_bricks, supported_by = drop_bricks(bricks)
    return len(safe_to_disintegrate(supported_by))


solution = Solution.from_file(__file__, process_lines, {TEST_INPUT: 5})

if __name__ == "__main__":
    solution.test_inputs()
    solution.submit()
