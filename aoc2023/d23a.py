import networkx as nx
import numpy as np
import numpy.typing as npt

from aoc2023.common import Solution
from aoc2023.grid import Point

TEST_INPUT = """\
#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
"""


def get_graph(lines: str) -> nx.DiGraph:
    maze = np.array([list(line) for line in lines.splitlines()])
    graph = nx.DiGraph()
    start = Point(0, 1)
    end = Point(maze.shape[0] - 1, maze.shape[1] - 2)
    graph.add_edge("start", start, weight=0)
    graph.add_edge(end, "end", weight=0)
    nodes_to_visit = [start]
    while nodes_to_visit:
        pos = nodes_to_visit.pop()
        connected_nodes = follow_path(maze, pos, start, end)
        for connected_node, path_len in connected_nodes:
            nodes_to_visit.append(connected_node)
            graph.add_edge(pos, connected_node, weight=path_len)
    return graph


def follow_path(
    maze: npt.NDArray[np.str_], entry: Point, start: Point, end: Point
) -> list[tuple[Point, int]]:
    directions = []
    if entry == start:
        directions = [Point(1, 0)]
    elif entry == end:
        return []
    else:
        if maze[entry.up().to_tuple()] == "^":
            directions.append(Point(-1, 0))
        if maze[entry.down().to_tuple()] == "v":
            directions.append(Point(1, 0))
        if maze[entry.left().to_tuple()] == "<":
            directions.append(Point(0, -1))
        if maze[entry.right().to_tuple()] == ">":
            directions.append(Point(0, 1))
    if not directions:
        raise ValueError(f"Could not find a direction from {entry}")
    return [
        follow_simple_path(maze, entry + direction, direction, end)
        for direction in directions
    ]


def follow_simple_path(
    maze: npt.NDArray[np.str_], entry: Point, direction: Point, end: Point
) -> tuple[Point, int]:
    last_move = direction
    path_len = 1
    pos = entry
    while True:
        if pos == end:
            return pos, path_len
        for new_move in [Point(1, 0), Point(-1, 0), Point(0, 1), Point(0, -1)]:
            if new_move == -1 * last_move:
                continue
            new_pos = pos + new_move
            if new_pos.y < 0 or new_pos.y >= maze.shape[0]:
                continue
            if new_pos.x < 0 or new_pos.x >= maze.shape[1]:
                continue
            if maze[*new_pos.to_tuple()] == "#":
                continue
            if maze[*new_pos.to_tuple()] == ".":
                path_len += 1
                pos = new_pos
                last_move = new_move
                break
            if maze[*new_pos.to_tuple()] in "^v<>":
                path_len += 2
                pos = new_pos + new_move
                last_move = new_move
                return pos, path_len
            raise ValueError(f"Unexpected maze character {maze[*new_pos.to_tuple()]}")
        else:
            raise ValueError(f"Could not find a new move from {entry}")


def longest_path(graph: nx.DiGraph) -> int:
    path: int = nx.algorithms.dag_longest_path_length(graph, weight="weight")
    return path


def process_lines(lines: str) -> int:
    return longest_path(get_graph(lines))


solution = Solution.from_file(__file__, process_lines, {TEST_INPUT: 94})

if __name__ == "__main__":
    solution.test_inputs()
    solution.submit()
