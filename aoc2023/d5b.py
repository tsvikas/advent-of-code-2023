import more_itertools
from aocd import data

from aoc2023.d5a import TEST_INPUT, Map, RangeMap, create_maps  # noqa: F401

SrcRange = tuple[int, int]
SrcRanges = list[SrcRange]


def use_range_map(
    range_map: RangeMap, src_ranges: SrcRanges
) -> tuple[SrcRanges, SrcRanges]:
    map_dst_start, map_src_start, map_length = range_map
    map_src_end = map_src_start + map_length
    map_change = map_dst_start - map_src_start
    passing = []
    remaining = []
    for src_range in src_ranges:
        src_range_start, src_range_end = src_range
        if src_range_end <= map_src_start or map_src_end <= src_range_start:
            remaining.append(src_range)
        elif map_src_start <= src_range_start <= src_range_end <= map_src_end:
            passing.append((src_range_start + map_change, src_range_end + map_change))
        else:
            # possible orders:
            # ss ms se me
            # ss ms me se
            # ms ss me se
            left_start = min(src_range_start, map_src_start)
            left_end = map_src_start
            right_start = map_src_end
            right_end = max(src_range_end, map_src_end)
            middle_start = max(src_range_start, map_src_start)
            middle_end = min(src_range_end, map_src_end)
            if left_start < left_end:
                remaining.append((left_start, left_end))
            if right_start < right_end:
                remaining.append((right_start, right_end))
            if middle_start < middle_end:
                passing.append((middle_start + map_change, middle_end + map_change))
    return passing, remaining


def use_map(maps: Map, src_ranges: SrcRanges):
    """
    >>> use_map([(50, 98, 2), (52, 50, 48)], [(79, 79+1)])
    [(81, 82)]
    >>> use_map([(0, 15, 37), (37, 52, 2), (39, 0, 15)], [(81, 81+1)])
    [(81, 82)]
    """

    passing = []
    remaining = src_ranges
    for range_map in maps:
        new_passing, remaining = use_range_map(range_map, remaining)
        passing.extend(new_passing)
    return passing + remaining


def use_maps(maps: dict[str, Map], src_ranges: SrcRanges):
    """
    >>> use_maps(create_maps(TEST_INPUT.splitlines()[2:]), [(79, 79+1)])
    [(82, 83)]
    >>> use_maps(create_maps(TEST_INPUT.splitlines()[2:]), [(14, 14+1)])
    [(43, 44)]
    >>> use_maps(create_maps(TEST_INPUT.splitlines()[2:]), [(55, 55+1)])
    [(86, 87)]
    >>> use_maps(create_maps(TEST_INPUT.splitlines()[2:]), [(13, 13+1)])
    [(35, 36)]
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
    [(60, 61), (86, 90), (94, 97), (82, 85), (56, 60), (46, 56), (97, 99)]
    """
    seeds_str = lines.pop(0).split(":")[1]
    seed_ints = [int(w) for w in seeds_str.split()]
    seed_ranges = [
        (start, start + length)
        for start, length in more_itertools.chunked(seed_ints, 2)
    ]

    assert lines.pop(0) == ""
    maps = create_maps(lines)
    seed_location_ranges = use_maps(maps, seed_ranges)
    return seed_location_ranges


def min_in_ranges(src_ranges: SrcRanges) -> int:
    """
    >>> min_in_ranges([(1, 2), (3, 4)])
    1
    >>> min_in_ranges([(3, 4), (1, 4)])
    1
    """
    return min(src_range[0] for src_range in src_ranges)


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
