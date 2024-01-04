from dataclasses import dataclass
from typing import Self

from aoc2023.common import Solution
from aoc2023.d19a import TEST_INPUT, Pipeline


@dataclass
class Range:
    min_value: int
    max_value: int

    @property
    def distinct_combinations(self) -> int:
        return self.max_value - self.min_value + 1

    @classmethod
    def range_or_none(cls, min_value: int, max_value: int) -> Self | None:
        if min_value > max_value:
            return None
        return cls(min_value, max_value)

    def cut(self, value: int, op: str) -> tuple[Self | None, Self | None]:
        cls = type(self)
        if op == "<":
            return (
                cls.range_or_none(self.min_value, value - 1),
                cls.range_or_none(value, self.max_value),
            )
        if op == ">":
            return (
                cls.range_or_none(value + 1, self.max_value),
                cls.range_or_none(self.min_value, value),
            )
        raise ValueError(f"illegal op {op!r}")


@dataclass
class PartRange:
    x: Range
    m: Range
    a: Range
    s: Range

    @classmethod
    def full_range(cls) -> Self:
        x = Range(1, 4000)
        m = Range(1, 4000)
        a = Range(1, 4000)
        s = Range(1, 4000)
        return cls(x, m, a, s)

    def cut(self, key: str, value: int, op: str) -> tuple[Self | None, Self | None]:
        range_key: Range = getattr(self, key)
        cut_ranges: tuple[Range | None, Range | None] = range_key.cut(value, op)
        part_ranges = tuple(
            None
            if cut_range is None
            else type(self)(
                x=cut_range if key == "x" else self.x,
                m=cut_range if key == "m" else self.m,
                a=cut_range if key == "a" else self.a,
                s=cut_range if key == "s" else self.s,
            )
            for cut_range in cut_ranges
        )
        assert len(part_ranges) == 2  # noqa: PLR2004
        return part_ranges

    @property
    def distinct_combinations(self) -> int:
        return (
            self.x.distinct_combinations
            * self.m.distinct_combinations
            * self.a.distinct_combinations
            * self.s.distinct_combinations
        )

    def use_rule(self, rule: str) -> tuple[Self | None, Self | None, str]:
        if ":" not in rule:
            return self, None, rule
        cond, ret = rule.split(":")
        key = cond[0]
        op = cond[1]
        value_s = cond[2:]
        value = int(value_s)
        range_true, range_false = self.cut(key, value, op)
        return range_true, range_false, ret

    def use_pipeline(self, pipeline: Pipeline) -> list[tuple[Self, str]]:
        part_ranges_and_results = []
        range_false: Self | None = self
        for rule in pipeline.rules:
            assert range_false is not None
            range_true, range_false, ret = range_false.use_rule(rule)
            if range_true is not None:
                part_ranges_and_results.append((range_true, ret))
            if range_false is None:
                break
        else:
            raise ValueError(f"no rule matched {range_false=} in {pipeline=}")
        return part_ranges_and_results


def use_pipelines(
    part_ranges_and_pipelines: list[tuple[PartRange, str]],
    pipelines: dict[str, Pipeline],
) -> list[tuple[PartRange, bool]]:
    part_ranges_and_pipelines = part_ranges_and_pipelines[:]
    part_ranges_finished = []
    while part_ranges_and_pipelines:
        part_range, pipeline_name = part_ranges_and_pipelines.pop()
        pipeline = pipelines[pipeline_name]
        part_ranges_and_results = part_range.use_pipeline(pipeline)
        part_ranges_and_pipelines.extend(
            [
                (part_range, pipeline_name)
                for part_range, pipeline_name in part_ranges_and_results
                if pipeline_name not in ["A", "R"]
            ]
        )
        part_ranges_finished.extend(
            [
                (part_range, accepted == "A")
                for part_range, accepted in part_ranges_and_results
                if accepted in ["A", "R"]
            ]
        )
    return part_ranges_finished


def process_lines(lines: str) -> int:
    pipelines_s, _parts_s = lines.split("\n\n")
    pipelines = dict(Pipeline.from_line(line) for line in pipelines_s.splitlines())
    part_ranges = [(PartRange.full_range(), "in")]
    part_ranges_and_accepted = use_pipelines(part_ranges, pipelines)
    return sum(
        part_range.distinct_combinations
        for part_range, accepted in part_ranges_and_accepted
        if accepted
    )


solution = Solution.from_file(__file__, process_lines, {TEST_INPUT: 167409079868000})

if __name__ == "__main__":
    solution.test_inputs()
    solution.submit()
