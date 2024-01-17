import itertools

import networkx as nx

from aoc2023.common import Solution
from aoc2023.d23a import TEST_INPUT, get_graph
from aoc2023.grid import Point


def get_undirected_graph(lines: str) -> nx.Graph:
    graph = nx.Graph()
    dag = get_graph(lines)
    for edge in dag.edges:
        graph.add_edge(edge[0], edge[1], weight=dag.edges[edge]["weight"])
    return graph


def path_length(graph: nx.Graph, path: list[Point]) -> int:
    path_len = 0
    for node1, node2 in itertools.pairwise(path):
        path_len += graph.edges[node1, node2]["weight"]
    return path_len


def remove_node(graph: nx.Graph, node: Point | str) -> nx.Graph:
    assert "end" in graph, "end not found"
    assert node != "end", "cannot remove end"
    new_graph = graph.copy()
    new_graph.remove_node(node)
    # return the component that contains end
    components = list(nx.connected_components(new_graph))
    for component in components:
        if "end" in component:
            # TODO: repeatdly remove all nodes that have degree 1, except start and end
            subgraph: nx.Graph = new_graph.subgraph(component)
            return subgraph
    assert False, "unreachable"  # noqa: B011


longest_path_cache: dict[tuple[frozenset[Point | str], Point | str], int] = {}


def longest_path(
    graph: nx.Graph,
    start: Point | str,
    current_path: int = 0,
    best_path: int | None = None,
) -> tuple[int | None, bool]:
    graph_nodes = frozenset(graph.nodes)
    if (graph_nodes, start) in longest_path_cache:
        return current_path + longest_path_cache[graph_nodes, start], True

    best_path, is_exact, changed = longest_path_(graph, start, current_path, best_path)

    if is_exact and changed:
        assert best_path is not None
        longest_path_cache[graph_nodes, start] = best_path - current_path
    return best_path, is_exact


def longest_path_(
    graph: nx.Graph,
    start: Point | str,
    current_path: int = 0,
    best_path: int | None = None,
) -> tuple[int | None, bool, bool | None]:
    if start == "end":
        return current_path, True, None

    if start not in graph or not graph[start]:
        return None, True, None

    if best_path is not None and current_path < best_path:
        best_case = current_path + sum(
            max(graph[n1][n2]["weight"] for n2 in graph[n1]) for n1 in graph
        )
        if best_case <= best_path:
            return None, False, None

    is_exact = True
    changed = False
    for node in graph[start]:
        path_len, is_exact_node = longest_path(
            remove_node(graph, start),
            node,
            current_path + graph[start][node]["weight"],
            best_path,
        )
        if path_len is not None and (best_path is None or path_len > best_path):
            is_exact = is_exact and is_exact_node
            best_path = path_len
            changed = True
    return best_path, is_exact, changed


def process_lines(lines: str) -> int:
    graph = get_undirected_graph(lines)
    best_path, is_exact = longest_path(graph, "start")
    return best_path or -1


solution = Solution.from_file(__file__, process_lines, {TEST_INPUT: 154})

if __name__ == "__main__":
    solution.test_inputs()
    solution.submit()
