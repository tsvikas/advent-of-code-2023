# can be used in 3, 10, 11, ...
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Optional, Self

import numpy as np
import numpy.typing as npt

PointTuple = tuple[int, int]


@dataclass(frozen=True)
class Point:
    y: int
    x: int

    def to_tuple(self) -> PointTuple:
        return self.y, self.x

    def __add__(self, other: "Point") -> Self:
        return type(self)(y=self.y + other.y, x=self.x + other.x)

    def __sub__(self, other: "Point") -> Self:
        return type(self)(self.y - other.y, self.x - other.x)

    def __mul__(self, other: int) -> Self:
        return type(self)(self.y * other, self.x * other)

    def __rmul__(self, other: int) -> Self:
        return self * other

    def manhattan_distance(self, other: Self) -> int:
        return abs(self.y - other.y) + abs(self.x - other.x)

    def __repr__(self) -> str:
        return f"P({self.y}, {self.x})"

    def up(self) -> Self:
        return self + Point(-1, 0)

    def down(self) -> Self:
        return self + Point(1, 0)

    def left(self) -> Self:
        return self + Point(0, -1)

    def right(self) -> Self:
        return self + Point(0, 1)

    def to_area(
        self, other: Optional["Point"] = None, expand: int = 0
    ) -> tuple[int, int, int, int]:
        if other is None:
            other = self
        left = max(0, min(self.x, other.x) - expand)
        right = max(self.x, other.x) + 1 + expand
        top = max(0, min(self.y, other.y) - expand)
        bottom = max(self.y, other.y) + 1 + expand
        return top, bottom, left, right


class Grid:
    def __init__(self, data: npt.NDArray[Any]):
        self.data = data

    def in_bounds(self, p: Point) -> bool:
        return 0 <= p.y < self.data.shape[0] and 0 <= p.x < self.data.shape[1]

    def __getitem__(self, item: Point | PointTuple) -> Any:
        if isinstance(item, Point):
            item = item.to_tuple()
        value: Any = self.data[item]
        return value

    @classmethod
    def from_string(cls, data: str) -> Self:
        return cls(np.array([list(line) for line in data.splitlines()]))

    def apply(self, f: Callable[[Any], Any]) -> Self:
        vf = np.vectorize(f)
        return type(self)(vf(self.data))

    def map_values(self, m: dict[Any, Any], default: Any | None = None) -> Self:
        if default is None:
            return self.apply(m.__getitem__)
        return self.apply(lambda x: m.get(x, default))

    def map_some_values(self, m: dict[Any, Any]) -> Self:
        return self.apply(lambda x: m.get(x, x))

    def where(self, f: Callable[[Any], np.bool_], other: Any | Self) -> Self:
        other_data = other.data if isinstance(other, Grid) else other
        cond: npt.NDArray[np.bool_] = self.apply(f).data
        return type(self)(np.where(cond, self.data, other_data))

    def find(self, value: Any) -> list[Point]:
        return [Point(*yx) for yx in np.argwhere(self.data == value)]

    def __str__(self) -> str:
        return "\n".join("".join(value) for value in self.data)

    def __repr__(self) -> str:
        return f"Grid({self.data!r})"

    def mark(self, yx: Point | PointTuple, value: Any) -> Self:
        y, x = yx.to_tuple() if isinstance(yx, Point) else yx
        data = self.data.copy()
        data[y, x] = value
        return type(self)(data)

    def slice(self, top: int, bottom: int, left: int, right: int) -> Self:  # noqa: A003
        return type(self)(self.data[top:bottom, left:right])

    def neighbours(
        self, yx: Point | PointTuple, *, include_diagonals: bool = True
    ) -> list[Any]:
        if include_diagonals:
            if not isinstance(yx, Point):
                yx = Point(*yx)
            area = self.slice(*yx.to_area(expand=1))
            area_values: list[Any] = area.data.flatten().tolist()
            return area_values
        y, x = yx.to_tuple() if isinstance(yx, Point) else yx
        neighbours = []
        for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            if 0 <= y + dy < self.data.shape[0] and 0 <= x + dx < self.data.shape[1]:
                neighbours.append(self.data[y + dy, x + dx])
        return neighbours


if __name__ == "__main__":
    from aocd import get_data  # type: ignore[attr-defined]

    grid = Grid.from_string(get_data(year=2023, day=10))
    m = dict(zip("-|F7LJ", "─│╭╮╰╯", strict=True))
    print(grid.map_some_values(m).mark(grid.find("S")[0], "*"))
