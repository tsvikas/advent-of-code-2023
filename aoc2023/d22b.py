import networkx as nx

from aoc2023.common import Solution
from aoc2023.d22a import TEST_INPUT, Brick, drop_bricks


def get_support_graph(
    falled_bricks: dict[int, Brick], supported_by: dict[int, set[int]]
) -> nx.DiGraph:
    graph = nx.DiGraph()
    for b, brick_supported_by in supported_by.items():
        for support in brick_supported_by:
            graph.add_edge(support, b)
    for b, brick in falled_bricks.items():
        graph.nodes[b]["subset"] = brick.end1.z
    graph.nodes[0]["subset"] = 0
    return graph


def bricks_falling(
    falled_bricks: dict[int, Brick], supported_by: dict[int, set[int]]
) -> dict[int, int]:
    graph = get_support_graph(falled_bricks, supported_by)
    num_falling = {}
    for brick in supported_by:
        after_remove = graph.copy()
        after_remove.remove_node(brick)
        non_falling: set[int] = nx.descendants(after_remove, 0)  # type: ignore[no-untyped-call]
        # (-1 for itself and -1 for the root)
        num_falling[brick] = len(graph) - len(non_falling) - 2
    return num_falling


def process_lines(lines: str) -> int:
    bricks = [Brick.from_line(line) for line in lines.splitlines()]
    falled_bricks, supported_by = drop_bricks(bricks)
    return sum(bricks_falling(falled_bricks, supported_by).values())


solution = Solution.from_file(__file__, process_lines, {TEST_INPUT: 7})

if __name__ == "__main__":
    solution.test_inputs()
    solution.submit()
