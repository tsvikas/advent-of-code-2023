from dataclasses import dataclass

import more_itertools
from aocd import data

from aoc2023.d5a import TEST_INPUT, RangeMap  # noqa: F401


@dataclass
class SrcRange:
    start: int
    length: int

    @property
    def end(self) -> int:
        return self.start + self.length

    def in_range(self, value: int) -> bool:
        return self.start <= value < self.end

    def __repr__(self) -> str:
        return f"{self.start}+{self.length}"


Map = list[RangeMap]
SrcRanges = list[SrcRange]


def create_maps(lines: list[str]) -> dict[str, Map]:
    maps_lines = more_itertools.split_at(lines, lambda line: line == "")
    maps = {
        map_lines[0].replace(" map:", ""): [
            RangeMap.from_line(map_line) for map_line in map_lines[1:]
        ]
        for map_lines in maps_lines
    }
    return maps


def use_range_map(
    range_map: RangeMap, src_ranges: SrcRanges
) -> tuple[SrcRanges, SrcRanges]:
    passing = []
    remaining = []
    for src_range in src_ranges:
        if (
            src_range.end <= range_map.source_range_start
            or range_map.source_range_end <= src_range.start
        ):
            remaining.append(src_range)
        elif (
            range_map.source_range_start
            <= src_range.start
            <= src_range.end
            <= range_map.source_range_end
        ):
            passing.append(
                SrcRange(
                    src_range.start + range_map.map_change,
                    src_range.length,
                )
            )
        else:
            # possible orders:
            # ss ms se me
            # ss ms me se
            # ms ss me se
            left_start = min(src_range.start, range_map.source_range_start)
            left_end = range_map.source_range_start
            right_start = range_map.source_range_end
            right_end = max(src_range.end, range_map.source_range_end)
            middle_start = max(src_range.start, range_map.source_range_start)
            middle_end = min(src_range.end, range_map.source_range_end)
            if left_start < left_end:
                remaining.append(SrcRange(left_start, left_end - left_start))
            if right_start < right_end:
                remaining.append(SrcRange(right_start, right_end - right_start))
            if middle_start < middle_end:
                passing.append(
                    SrcRange(
                        middle_start + range_map.map_change,
                        middle_end - middle_start,
                    )
                )
    return passing, remaining


def use_map(maps: Map, src_ranges: SrcRanges):
    """
    >>> maps = create_maps(TEST_INPUT.splitlines()[2:])
    >>> use_map(maps["seed-to-soil"], [SrcRange(79, 1)])
    [81+1]
    >>> use_map(maps["soil-to-fertilizer"], [SrcRange(81, 1)])
    [81+1]
    """

    passing = []
    remaining = src_ranges
    for range_map in maps:
        new_passing, remaining = use_range_map(range_map, remaining)
        passing.extend(new_passing)
    return passing + remaining


def use_maps(maps: dict[str, Map], src_ranges: SrcRanges):
    """
    >>> maps = create_maps(TEST_INPUT.splitlines()[2:])
    >>> use_maps(maps, [SrcRange(79, 1)])
    [82+1]
    >>> use_maps(maps, [SrcRange(14, 1)])
    [43+1]
    >>> use_maps(maps, [SrcRange(55, 1)])
    [86+1]
    >>> use_maps(maps, [SrcRange(13, 1)])
    [35+1]
    """
    current_ranges = src_ranges
    current_type = "seed"
    for map_name, map_lines in maps.items():
        assert map_name.startswith(f"{current_type}-to-")
        current_ranges = use_map(map_lines, current_ranges)
        current_type = map_name.split("-to-")[1]
    assert current_type == "location"
    return current_ranges


def find_location_ranges_from_seed_ranges(lines: list[str]) -> SrcRanges:
    """
    >>> find_location_ranges_from_seed_ranges(TEST_INPUT.splitlines())
    [60+1, 86+4, 94+3, 82+3, 56+4, 46+10, 97+2]
    """
    seeds_str = lines.pop(0).split(":")[1]
    seed_ints = [int(w) for w in seeds_str.split()]
    seed_ranges = [
        SrcRange(start, length)
        for start, length in more_itertools.chunked(seed_ints, 2)
    ]

    assert lines.pop(0) == ""
    maps = create_maps(lines)
    seed_location_ranges = use_maps(maps, seed_ranges)
    return seed_location_ranges


def min_in_ranges(src_ranges: SrcRanges) -> int:
    """
    >>> min_in_ranges([SrcRange(1, 2), SrcRange(3, 2)])
    1
    >>> min_in_ranges([SrcRange(3, 7), SrcRange(1, 7)])
    1
    """
    return min(src_range.start for src_range in src_ranges)


def process_lines(lines: list[str]) -> int:
    """
    >>> process_lines(TEST_INPUT.splitlines())
    46
    """
    return min_in_ranges(find_location_ranges_from_seed_ranges(lines))


def main() -> int:
    lines = data.splitlines()
    result = process_lines(lines)
    return result


if __name__ == "__main__":
    print(main())
