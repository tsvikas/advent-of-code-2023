from collections.abc import Iterable

import sympy

from aoc2023.common import Solution
from aoc2023.d24a import TEST_INPUT, HailStone


def find_crossing_rock(hail_stones: Iterable[HailStone]) -> HailStone:
    hail_stones = list(hail_stones)
    equations = []
    x, y, z = sympy.symbols("x y z")
    vx, vy, vz = sympy.symbols("vx vy vz")
    symbols = [x, y, z, vx, vy, vz]
    t: dict[int, sympy.Symbol] = {}
    for i, stone in enumerate(hail_stones):
        t[i] = sympy.Symbol(f"t{i}")  # type: ignore[no-untyped-call]
        equations += [
            x + vx * t[i] - (stone.x + stone.vx * t[i]),
            y + vy * t[i] - (stone.y + stone.vy * t[i]),
            z + vz * t[i] - (stone.z + stone.vz * t[i]),
        ]
        symbols += [t[i]]
        if len(symbols) <= len(equations):
            solutions: list[dict[sympy.Symbol, float]]
            solutions = sympy.solve(equations[:9], symbols[:9], dict=True)  # type: ignore[no-untyped-call]
            if solutions:
                break
    else:
        raise ValueError("No solution found")
    sol = solutions[0]
    return HailStone(
        int(sol[x]), int(sol[y]), int(sol[z]), int(sol[vx]), int(sol[vy]), int(sol[vz])
    )


def process_lines(lines: str) -> int:
    return sum(
        find_crossing_rock(
            HailStone.from_line(line) for line in lines.splitlines()
        ).position
    )


solution = Solution.from_file(__file__, process_lines, {TEST_INPUT: 47})

if __name__ == "__main__":
    solution.test_inputs()
    solution.submit()
