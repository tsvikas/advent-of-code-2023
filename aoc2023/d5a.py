from dataclasses import dataclass

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


@dataclass
class RangeMap:
    destination_range_start: int
    source_range_start: int
    range_length: int

    @property
    def destination_range_end(self) -> int:
        return self.destination_range_start + self.range_length

    @property
    def source_range_end(self) -> int:
        return self.source_range_start + self.range_length

    @property
    def map_change(self) -> int:
        return self.destination_range_start - self.source_range_start

    def in_range(self, value: int) -> bool:
        return self.source_range_start <= value < self.source_range_end

    @classmethod
    def from_line(cls, line: str) -> "RangeMap":
        return cls(*[int(w) for w in line.split()])


@dataclass
class Map:
    range_maps: list[RangeMap]

    @classmethod
    def from_lines(cls, lines: list[str]) -> "Map":
        return cls([RangeMap.from_line(line) for line in lines])

    def pass_value(self, value: int) -> int:
        """
        >>> map_ranges = Map([RangeMap(50, 98, 2), RangeMap(52, 50, 48)])
        >>> values = [0, 1, 48, 49, 50, 51, 96, 97, 98, 99]
        >>> [map_ranges.pass_value(value) for value in values]
        [0, 1, 48, 49, 52, 53, 98, 99, 50, 51]
        >>> [map_ranges.pass_value(value) for value in [79, 14, 55, 13]]
        [81, 14, 57, 13]
        """
        for range_map in self.range_maps:
            if range_map.in_range(value):
                return value + range_map.map_change
        return value


def create_maps(lines: list[str]) -> dict[str, Map]:
    maps_lines = more_itertools.split_at(lines, lambda line: line == "")
    maps = {
        map_lines[0].replace(" map:", ""): Map.from_lines(map_lines[1:])
        for map_lines in maps_lines
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
    >>> maps = create_maps(TEST_INPUT.splitlines()[2:])
    >>> find_location_from_seed(maps, 79)
    82
    >>> find_location_from_seed(maps, 14)
    43
    >>> find_location_from_seed(maps, 55)
    86
    >>> find_location_from_seed(maps, 13)
    35
    """
    current_value = seed
    current_type = "seed"
    for map_name, map_lines in maps.items():
        assert map_name.startswith(f"{current_type}-to-")
        current_value = map_lines.pass_value(current_value)
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
