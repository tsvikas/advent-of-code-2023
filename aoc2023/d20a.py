import math
from collections import defaultdict
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Self

import matplotlib.pyplot as plt
import networkx as nx

from aoc2023.common import Solution

TEST_INPUT = """\
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
"""
TEST_INPUT_2 = """\
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
"""


class ModuleType(StrEnum):
    FLIP_FLOP = "%"
    CONJUNCTION = "&"
    BROADCASTER = "broadcaster"


ModulesState = tuple[
    tuple[tuple[str, bool], ...], tuple[tuple[str, frozenset[str]], ...]
]


@dataclass
class Modules:
    modules: dict[str, ModuleType]
    cables: dict[str, list[str]]
    memory_flipflop: dict[str, bool]
    memory_conjunction: dict[str, set[str]]
    module_num_inputs: dict[str, int] = field(init=False)
    signals: list[tuple[str, str, str]] = field(default_factory=list)
    signals_low: int = 0
    signals_high: int = 0
    button_pressed: int = 0

    def __post_init__(self) -> None:
        self.module_num_inputs = defaultdict(int)
        for target_names in self.cables.values():
            for target_name in target_names:
                self.module_num_inputs[target_name] += 1

    def to_graph(self, *, only_conj: bool = False) -> nx.DiGraph:
        graph = nx.DiGraph()
        for module_name, module_type in self.modules.items():
            if not only_conj or module_type == ModuleType.CONJUNCTION:
                graph.add_node(module_name, type=module_type)
        for source, targets in self.cables.items():
            for target in targets:
                if (
                    not only_conj
                    or self.modules[source] == ModuleType.CONJUNCTION
                    and (
                        target == "rx" or self.modules[target] == ModuleType.CONJUNCTION
                    )
                ):
                    graph.add_edge(source, target)
        return graph

    def plot_graph(self, *, only_conj: bool = False) -> None:
        color_map = {
            "broadcaster": "blue",
            "%": "green",
            "&": "red",
            "": "yellow",
        }
        g = self.to_graph(only_conj=only_conj)
        colors = [color_map[g.nodes[node].get("type", "")] for node in g]
        node_pos = nx.planar_layout(g, scale=1)
        nx.draw(g, node_color=colors, with_labels=True, pos=node_pos)
        plt.show()

    @classmethod
    def from_lines(cls, lines: str) -> Self:
        arrow = " -> "
        modules: dict[str, ModuleType] = {}
        cables: dict[str, list[str]] = {}
        memory_flipflop: dict[str, bool] = {}
        memory_conjunction: dict[str, set[str]] = {}
        for line in lines.splitlines():
            assert arrow in line
            source, targets = line.split(arrow)
            module_type = ModuleType(
                "broadcaster" if source == "broadcaster" else source[0]
            )
            module_name = "broadcaster" if source == "broadcaster" else source[1:]
            target_names = targets.split(", ")
            modules[module_name] = module_type
            cables[module_name] = target_names
            if module_type == ModuleType.FLIP_FLOP:
                memory_flipflop[module_name] = False
            if module_type == ModuleType.CONJUNCTION:
                memory_conjunction[module_name] = set()
        return cls(modules, cables, memory_flipflop, memory_conjunction)

    def freeze_memory(
        self,
    ) -> ModulesState:
        memory_flipflop = tuple((k, v) for k, v in self.memory_flipflop.items())
        memory_conjunction = tuple(
            (k, frozenset(v)) for k, v in self.memory_conjunction.items()
        )
        return memory_flipflop, memory_conjunction

    def press_button(self, n: int) -> tuple[int, int]:
        cache: dict[ModulesState, tuple[int, int, int]] = {}
        for _ in range(n):
            state = self.freeze_memory()
            if state in cache:
                remaining_presses = n - self.button_pressed
                cycle = self.button_pressed - cache[state][0]
                if remaining_presses % cycle == 0:
                    remaining_cycles = remaining_presses // cycle
                    low_per_cycle = self.signals_low - cache[state][1]
                    high_per_cycle = self.signals_high - cache[state][2]
                    self.signals_low += low_per_cycle * remaining_cycles
                    self.signals_high += high_per_cycle * remaining_cycles
                    return self.signals_low, self.signals_high
            cache[state] = self.button_pressed, self.signals_low, self.signals_high
            self.signals.append(("button", "low", "broadcaster"))
            self.button_pressed += 1
            self.process_signals()
        return self.signals_low, self.signals_high

    def rx_low_count(self) -> int:
        assert "rx" in self.module_num_inputs
        pointing_to_rx = [
            module for module, targets in self.cables.items() if "rx" in targets
        ]
        assert len(pointing_to_rx) == 1
        target = pointing_to_rx[0]
        modules_to_measure = {
            module: 0 for module, targets in self.cables.items() if target in targets
        }
        assert all(
            self.modules[module] == ModuleType.CONJUNCTION
            for module in modules_to_measure
        )
        self.signals.append(("button", "low", "broadcaster"))
        self.button_pressed += 1
        _changed_modules = self.process_signals()
        while True:
            self.signals.append(("button", "low", "broadcaster"))
            self.button_pressed += 1
            changed_modules = self.process_signals()
            for module in changed_modules:
                if modules_to_measure.get(module, -1) == 0:
                    modules_to_measure[module] = self.button_pressed
            if all(modules_to_measure.values()):
                return math.prod(modules_to_measure.values())

    def send_from(self, source: str, signal: str) -> None:
        for target in self.cables[source]:
            self.signals.append((source, signal, target))

    def process_signals(  # noqa: PLR0912
        self, *, print_signals: bool = False
    ) -> set[str]:
        changed_modules = set()
        while self.signals:
            source, signal, target = self.signals.pop(0)
            if signal == "low":
                self.signals_low += 1
            elif signal == "high":
                self.signals_high += 1
            else:
                raise ValueError(f"illegal signal {signal}")
            if print_signals:
                print(f"{source} -{signal}-> {target}")
            if target not in self.modules:
                continue
            match self.modules[target]:
                case ModuleType.BROADCASTER:
                    self.send_from(target, signal)
                case ModuleType.FLIP_FLOP:
                    if signal == "high":
                        pass
                    elif signal == "low":
                        self.memory_flipflop[target] = not self.memory_flipflop[target]
                        self.send_from(
                            target,
                            {True: "high", False: "low"}[self.memory_flipflop[target]],
                        )
                    else:
                        raise ValueError(f"illegal signal {signal}")
                case ModuleType.CONJUNCTION:
                    last_conj = (
                        len(self.memory_conjunction[target])
                        == self.module_num_inputs[target]
                    )
                    if signal == "high":
                        self.memory_conjunction[target].add(source)
                    elif signal == "low":
                        if source in self.memory_conjunction[target]:
                            self.memory_conjunction[target].remove(source)
                    else:
                        raise ValueError(f"illegal signal {signal}")
                    # send low pulse if all inputs are high
                    new_conj = (
                        len(self.memory_conjunction[target])
                        == self.module_num_inputs[target]
                    )
                    if new_conj != last_conj:
                        changed_modules.add(target)
                    if new_conj:
                        self.send_from(target, "low")
                    else:
                        self.send_from(target, "high")
                case _:
                    raise ValueError(f"illegal module type {self.modules[target]}")
        return changed_modules


def process_lines(lines: str) -> int:
    return math.prod(Modules.from_lines(lines).press_button(1000))


solution = Solution.from_file(
    __file__, process_lines, {TEST_INPUT: 32000000, TEST_INPUT_2: 11687500}
)

if __name__ == "__main__":
    solution.test_inputs()
    solution.submit()
