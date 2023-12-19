from dataclasses import dataclass
from typing import Self

from aocd import data

TEST_INPUT = """\
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
"""


@dataclass
class Pipeline:
    rules: list[str]

    @classmethod
    def from_line(cls, line: str) -> tuple[str, Self]:
        name, rules_s = line.split("{")
        rules = rules_s[:-1].split(",")
        return name, cls(rules)


@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int

    @classmethod
    def from_line(cls, line: str) -> Self:
        xs, ms, as_, ss = line[1:-1].split(",")
        x = int(xs.split("=")[1])
        m = int(ms.split("=")[1])
        a = int(as_.split("=")[1])
        s = int(ss.split("=")[1])
        return cls(x, m, a, s)

    @property
    def all_ratings(self) -> int:
        return self.x + self.m + self.a + self.s

    def use_rule(self, rule: str) -> str | None:
        if ":" not in rule:
            return rule
        cond, ret = rule.split(":")
        key = cond[0]
        op = cond[1]
        value_s = cond[2:]
        right = int(value_s)
        left = getattr(self, key)
        match op:
            case "<":
                return ret if left < right else None
            case ">":
                return ret if left > right else None
            case _:
                raise ValueError(f"illegal op {op!r}")

    def use_pipeline(self, pipeline: Pipeline) -> str:
        for rule in pipeline.rules:
            if ret := self.use_rule(rule):
                return ret
        raise ValueError(f"no rule matched {self=} in {pipeline=}")

    def use_pipelines(self, pipelines: dict[str, Pipeline]) -> bool:
        last_result = "in"
        while last_result not in ["A", "R"]:
            last_result = self.use_pipeline(pipelines[last_result])
        return last_result == "A"


def process_lines(lines: str) -> int:
    """
    >>> process_lines(TEST_INPUT)
    19114
    """
    pipelines_s, parts_s = lines.split("\n\n")
    parts = [Part.from_line(line) for line in parts_s.splitlines()]
    pipelines = dict(Pipeline.from_line(line) for line in pipelines_s.splitlines())
    return sum(part.all_ratings for part in parts if part.use_pipelines(pipelines))


def main() -> int:
    lines = data
    result = process_lines(lines)
    return result


if __name__ == "__main__":
    print(main())
