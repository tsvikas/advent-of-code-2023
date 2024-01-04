import math

import networkx as nx

from aoc2023.common import Solution

TEST_INPUT = """\
jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr
"""


def graph_from_lines(lines: str) -> nx.Graph:
    graph = nx.Graph()
    for line in lines.splitlines():
        src, dsts = line.split(": ")
        for dst in dsts.split(" "):
            graph.add_edge(src, dst)
    return graph


def cut_graph(graph: nx.Graph) -> list[int]:
    """
    >>> cut_graph(graph_from_lines(TEST_INPUT))
    [6, 9]
    """
    graph = graph.copy()
    edges_to_cut = nx.minimum_edge_cut(graph)
    for src, dst in edges_to_cut:
        graph.remove_edge(src, dst)

    return [len(component) for component in nx.components.connected_components(graph)]


def process_lines(lines: str) -> int:
    return math.prod(cut_graph(graph_from_lines(lines)))


solution = Solution.from_file(__file__, process_lines, {TEST_INPUT: 54})

if __name__ == "__main__":
    solution.test_inputs()
    solution.submit()
