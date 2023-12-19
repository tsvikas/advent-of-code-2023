from dataclasses import dataclass
from typing import Self

import networkx as nx
from aocd import data, submit  # type: ignore[attr-defined]

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

    def to_graph(self, min_line: int = 1, max_line: int = 3) -> nx.DiGraph:
        # create a graph:
        graph = nx.DiGraph()
        # add nodes:
        graph.add_edge("start", (0, 0, 0, 0), weight=0)
        for row, line in enumerate(self.data):
            for col, char in enumerate(line):
                for sign in [-1, 1]:
                    # from above/below, after change direction
                    for distance in range(min_line, max_line + 1):
                        graph.add_edge(
                            (row - sign, col, 0, distance),
                            (row, col, sign, 0),
                            weight=int(char),
                        )
                        graph.add_edge(
                            (row - sign, col, 0, -distance),
                            (row, col, sign, 0),
                            weight=int(char),
                        )
                    # from above/below, after a straight line
                    for distance in range(max_line):
                        graph.add_edge(
                            (row - sign, col, sign * distance, 0),
                            (row, col, sign * (distance + 1), 0),
                            weight=int(char),
                        )
                    # from left/right, after change direction
                    for distance in range(min_line, max_line + 1):
                        graph.add_edge(
                            (row, col - sign, distance, 0),
                            (row, col, 0, sign),
                            weight=int(char),
                        )
                        graph.add_edge(
                            (row, col - sign, -distance, 0),
                            (row, col, 0, sign),
                            weight=int(char),
                        )
                    # from left/right, after a straight line
                    for distance in range(max_line):
                        graph.add_edge(
                            (row, col - sign, 0, sign * distance),
                            (row, col, 0, sign * (distance + 1)),
                            weight=int(char),
                        )
        y_end = len(self.data) - 1
        x_end = len(self.data[0]) - 1
        for distance in range(min_line, max_line + 1):
            graph.add_edge((y_end, x_end, 0, distance), "end", weight=0)
            graph.add_edge((y_end, x_end, 0, -distance), "end", weight=0)
            graph.add_edge((y_end, x_end, distance, 0), "end", weight=0)
            graph.add_edge((y_end, x_end, -distance, 0), "end", weight=0)
        return graph

    def least_heat_loss(self, min_line: int = 1, max_line: int = 3) -> int:
        graph = self.to_graph(min_line, max_line)
        shortest_path_length: int = nx.shortest_path_length(
            graph,
            "start",
            "end",
            weight="weight",
        )
        return shortest_path_length


def process_lines(lines: str) -> int:
    """
    >>> process_lines(TEST_INPUT)
    102
    """
    return HeatGrid.from_line(lines).least_heat_loss()


def main() -> int:
    return process_lines(data)


if __name__ == "__main__":
    submit(main(), part=__file__[-4])
