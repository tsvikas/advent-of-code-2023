import itertools
from collections.abc import Generator
from dataclasses import dataclass
from typing import Any, Self

import igraph as ig  # type: ignore[import-untyped]

from aoc2023.common import Solution

TEST_INPUT = """\
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
"""


@dataclass
class HeatGrid:
    data: list[str]

    @classmethod
    def from_line(cls, line: str) -> Self:
        return cls(line.splitlines())

    def get_weighted_edges(
        self, min_line: int = 1, max_line: int = 3
    ) -> Generator[tuple[Any, Any, int], None, None]:
        # most nodes are of the form (y, x, last_dy, last_dx)
        for row, line in enumerate(self.data):
            for col, char in enumerate(line):
                # add edges from (*, *, *, *) to (row, col, *, *)
                c = int(char)
                for sign in [-1, 1]:
                    # after change direction
                    for distance in itertools.chain(
                        range(min_line, max_line + 1),
                        range(-min_line, -max_line - 1, -1),
                    ):
                        # from above/below
                        yield (
                            (row - sign, col, 0, distance),
                            (row, col, sign, 0),
                            c,
                        )
                        # from left/right
                        yield (
                            (row, col - sign, distance, 0),
                            (row, col, 0, sign),
                            c,
                        )
                    # after a straight line
                    for distance in range(max_line):
                        # from above/below
                        yield (
                            (row - sign, col, sign * distance, 0),
                            (row, col, sign * (distance + 1), 0),
                            c,
                        )
                        # from left/right
                        yield (
                            (row, col - sign, 0, sign * distance),
                            (row, col, 0, sign * (distance + 1)),
                            c,
                        )
        yield "start", (0, 0, 0, 0), 0
        y_end = len(self.data) - 1
        x_end = len(self.data[0]) - 1
        for distance in range(min_line, max_line + 1):
            yield (y_end, x_end, 0, +distance), "end", 0
            yield (y_end, x_end, 0, -distance), "end", 0
            yield (y_end, x_end, +distance, 0), "end", 0
            yield (y_end, x_end, -distance, 0), "end", 0

    def to_graph(self, min_line: int = 1, max_line: int = 3) -> ig.Graph:
        edges_w = list(self.get_weighted_edges(min_line, max_line))
        edges = [(str(edge[0]), str(edge[1])) for edge in edges_w]
        weights = [edge[2] for edge in edges_w]
        nodes = list({edge[0] for edge in edges} | {edge[1] for edge in edges})

        graph = ig.Graph(directed=True)
        graph.add_vertices(nodes)
        graph.add_edges(edges, attributes={"weight": weights})
        return graph

    def least_heat_loss(self, min_line: int = 1, max_line: int = 3) -> int:
        graph = self.to_graph(min_line, max_line)
        shortest_path_length = int(
            graph.distances("start", "end", weights="weight")[0][0]
        )
        return shortest_path_length


def process_lines(lines: str) -> int:
    return HeatGrid.from_line(lines).least_heat_loss()


solution = Solution.from_file(__file__, process_lines, {TEST_INPUT: 102})

if __name__ == "__main__":
    solution.test_inputs()
    solution.submit()
