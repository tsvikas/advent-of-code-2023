import more_itertools
from aocd import data

TEST_INPUT = """\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""
RangeMap = tuple[int, int, int]
Map = list[RangeMap]


def use_map(map_lines: Map, value: int) -> int:
    """
    >>> use_map([(50, 98, 2), (52, 50, 48)], 0)
    0
    >>> use_map([(50, 98, 2), (52, 50, 48)], 1)
    1
    >>> use_map([(50, 98, 2), (52, 50, 48)], 48)
    48
    >>> use_map([(50, 98, 2), (52, 50, 48)], 49)
    49
    >>> use_map([(50, 98, 2), (52, 50, 48)], 50)
    52
    >>> use_map([(50, 98, 2), (52, 50, 48)], 51)
    53
    >>> use_map([(50, 98, 2), (52, 50, 48)], 96)
    98
    >>> use_map([(50, 98, 2), (52, 50, 48)], 97)
    99
    >>> use_map([(50, 98, 2), (52, 50, 48)], 98)
    50
    >>> use_map([(50, 98, 2), (52, 50, 48)], 99)
    51
    >>> use_map([(50, 98, 2), (52, 50, 48)], 79)
    81
    >>> use_map([(50, 98, 2), (52, 50, 48)], 14)
    14
    >>> use_map([(50, 98, 2), (52, 50, 48)], 55)
    57
    >>> use_map([(50, 98, 2), (52, 50, 48)], 13)
    13
    """
    for line in map_lines:
        destination_range_start, source_range_start, range_length = line
        if source_range_start <= value < source_range_start + range_length:
            return destination_range_start + value - source_range_start
    return value


def create_maps(lines: list[str]) -> dict[str, Map]:
    map_strs = more_itertools.split_at(lines, lambda line: line == "")
    maps = {
        map_str[0].replace(" map:", ""): [
            tuple(int(w) for w in map_line.split()) for map_line in map_str[1:]
        ]
        for map_str in map_strs
    }
    return maps


def find_location_from_seeds(lines: list[str]) -> list[int]:
    """
    >>> find_location_from_seeds(TEST_INPUT.splitlines())
    [82, 43, 86, 35]
    """
    seeds = [int(w) for w in lines.pop(0).split(":")[1].split()]
    assert lines.pop(0) == ""
    maps = create_maps(lines)
    seed_locations = {seed: find_location_from_seed(maps, seed) for seed in seeds}
    return list(seed_locations.values())


def find_location_from_seed(maps: dict[str, Map], seed: int) -> int:
    """
    >>> find_location_from_seed(create_maps(TEST_INPUT.splitlines()[2:]), 79)
    82
    >>> find_location_from_seed(create_maps(TEST_INPUT.splitlines()[2:]), 14)
    43
    >>> find_location_from_seed(create_maps(TEST_INPUT.splitlines()[2:]), 55)
    86
    >>> find_location_from_seed(create_maps(TEST_INPUT.splitlines()[2:]), 13)
    35
    """
    current_value = seed
    current_type = "seed"
    for map_name, map_lines in maps.items():
        assert map_name.startswith(f"{current_type}-to-")
        current_value = use_map(map_lines, current_value)
        current_type = map_name.split("-to-")[1]
    assert current_type == "location"
    return current_value


def process_lines(lines: list[str]) -> int:
    """
    >>> process_lines(TEST_INPUT.splitlines())
    35
    """
    return min(find_location_from_seeds(lines))


def main() -> int:
    lines = data.splitlines()
    result = process_lines(lines)
    return result


if __name__ == "__main__":
    print(main())
