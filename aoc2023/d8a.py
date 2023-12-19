import itertools
import re
from dataclasses import dataclass
from typing import Self

from aoc2023.common import Solution

TEST_INPUT_1 = """\
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""

TEST_INPUT_2 = """\
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""


Direction = str
Node = str


@dataclass
class Page:
    instructions: list[Direction]
    network: dict[Node, dict[Direction, Node]]

    @classmethod
    def from_lines(cls, lines: list[str]) -> Self:
        instructions = list(lines[0])
        network = {}
        for line in lines[2:]:
            node, *connections = re.findall(r"(\w+)", line)
            network[node] = dict(zip("LR", connections, strict=True))
        return cls(instructions, network)

    def steps_to_end(self) -> int:
        node = "AAA"
        for i, instruction in enumerate(itertools.cycle(self.instructions)):
            if node == "ZZZ":
                return i
            node = self.network[node][instruction]
        raise RuntimeError("Unreachable")


def process_lines(lines: str) -> int:
    return Page.from_lines(lines.splitlines()).steps_to_end()


solution = Solution.from_file(
    __file__, process_lines, {TEST_INPUT_1: 2, TEST_INPUT_2: 6}
)

if __name__ == "__main__":
    solution.submit()
