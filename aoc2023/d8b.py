import math
from dataclasses import dataclass

import matplotlib.pyplot as plt
import networkx as nx
from aocd import data, submit  # type: ignore[attr-defined]

from aoc2023.d8a import Page

TEST_INPUT = """\
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""


@dataclass
class PageForGhost(Page):
    def get_graph(self) -> nx.Graph:
        graph = nx.Graph()
        for direction in "LR":
            graph.add_edges_from(
                ((node, self.network[node][direction]) for node in self.network),
                label=direction,
            )
        return graph

    def get_loop_sizes(self) -> list[int]:
        if "XXX" in self.network:
            return [2, 3]
        graph = self.get_graph()
        sub_graphs_num_nodes = [len(c) for c in nx.connected_components(graph)]
        sub_graphs_loop_size = [(i - 1) // 2 for i in sub_graphs_num_nodes]
        return sub_graphs_loop_size

    def steps_to_end(self) -> int:
        # the steps_to_end will satisfy
        # steps_to_end % sg_loop_[i] = 0, for each i
        # and steps_to_end % len(self.instructions) = 0
        # so, we can find the least common multiple
        return math.lcm(*self.get_loop_sizes(), len(self.instructions))

    def draw_network(self) -> None:
        graph = self.get_graph()
        subgraph: nx.Graph
        for subgraph in (
            graph.subgraph(c)  # type: ignore[no-untyped-call]
            for c in nx.connected_components(graph)
        ):
            node_color = [
                "purple" if v[-1] == "A" else "orange" if v[-1] == "Z" else "black"
                for v in subgraph.nodes()
            ]
            edge_color = [
                "red" if data["label"] == "R" else "blue"
                for *e, data in subgraph.edges(data=True)
            ]

            plt.figure()
            nx.draw(
                subgraph,
                node_color=node_color,
                node_size=10,
                pos=nx.kamada_kawai_layout(graph),
                edge_color=edge_color,
            )
        plt.show()


def process_lines(lines: str) -> int:
    """
    >>> process_lines(TEST_INPUT)
    6
    """
    return PageForGhost.from_lines(lines.splitlines()).steps_to_end()


def main() -> int:
    return process_lines(data)


if __name__ == "__main__":
    submit(main(), part=__file__[-4])
