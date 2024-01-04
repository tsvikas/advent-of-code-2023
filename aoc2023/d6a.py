import math
from dataclasses import dataclass

from aoc2023.common import Solution

TEST_INPUT = """\
Time:      7  15   30
Distance:  9  40  200
"""


@dataclass
class Race:
    time: int
    distance: int

    def n_ways_to_beat(self) -> int:
        """
        >>> Race(7, 9).n_ways_to_beat()
        4
        >>> Race(15, 40).n_ways_to_beat()
        8
        >>> Race(30, 200).n_ways_to_beat()
        9
        """
        # if we hold for t0, we got v = t0, x = v * dt = t0 (t-t0)
        # we win if t0 (t-t0) > d
        # so, t0^2 - t0*t + d < 0
        # so, (t - sqrt(t^2 - 4d))/2 < t0 < (t + sqrt(t^2 - 4d))/2
        # so, floor((t - sqrt(t^2 - 4d))/2) < t0 < ceil((t + sqrt(t^2 - 4d))/2)
        mantisa = math.sqrt(self.time**2 - 4 * self.distance)
        left = math.floor((self.time - mantisa) / 2)
        right = math.ceil((self.time + mantisa) / 2)
        return right - left - 1


def parse_lines(lines: list[str]) -> list[Race]:
    """
    >>> parse_lines(TEST_INPUT.splitlines())
    [Race(time=7, distance=9), Race(time=15, distance=40), Race(time=30, distance=200)]
    """
    times = [int(x) for x in lines[0].split()[1:]]
    distances = [int(x) for x in lines[1].split()[1:]]
    return [Race(t, d) for t, d in zip(times, distances, strict=True)]


def process_lines(lines: str) -> int:
    return math.prod(race.n_ways_to_beat() for race in parse_lines(lines.splitlines()))


solution = Solution.from_file(__file__, process_lines, {TEST_INPUT: 288})

if __name__ == "__main__":
    solution.test_inputs()
    solution.submit()
