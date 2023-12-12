import functools

from aocd import data

TEST_INPUTS = [
    "???.### 1,1,3",
    ".??..??...?##. 1,1,3",
    "?#?#?#?#?#?#?#? 1,3,1,6",
    "????.#...#... 4,1,1",
    "????.######..#####. 1,6,5",
    "?###???????? 3,2,1",
]
TEST_INPUTS_2 = [
    "???.###????.###????.###????.###????.### 1,1,3,1,1,3,1,1,3,1,1,3,1,1,3",
    "?###??????????###??????????###??????????###??????????###???????? "
    "3,2,1,3,2,1,3,2,1,3,2,1,3,2,1",
]


@functools.cache
def count_arrangements(  # noqa: PLR0911
    hot_springs: str, group_sizes: tuple[int, ...], *, required_start: str = ""
) -> int:
    """
    >>> [count_arrangements(*parse(line)) for line in TEST_INPUTS]
    [1, 4, 1, 1, 4, 10]
    >>> [count_arrangements(*parse(line)) for line in TEST_INPUTS_2]
    [1, 506250]
    """
    assert required_start in {"", ".", "#"}
    assert not group_sizes or group_sizes[0] > 0
    if not hot_springs:
        if group_sizes:
            return 0
        assert required_start != "#"
        return 1
    match hot_springs[0]:
        case ".":
            if required_start == "#":
                return 0
            return count_arrangements(hot_springs[1:], group_sizes, required_start="")
        case "#":
            if required_start == ".":
                return 0
            if not group_sizes:
                return 0
            if group_sizes[0] == 1:
                return count_arrangements(
                    hot_springs[1:], group_sizes[1:], required_start="."
                )
            new_group_sizes = (group_sizes[0] - 1, *group_sizes[1:])
            return count_arrangements(
                hot_springs[1:], new_group_sizes, required_start="#"
            )
        case "?":
            return count_arrangements(
                "." + hot_springs[1:], group_sizes, required_start=required_start
            ) + count_arrangements(
                "#" + hot_springs[1:], group_sizes, required_start=required_start
            )
    raise RuntimeError("unreachable")


def parse(line: str) -> tuple[str, tuple[int, ...]]:
    """
    >>> parse(TEST_INPUTS[0])
    ('???.###', (1, 1, 3))
    """
    s1, s2 = line.split()
    return s1, tuple(int(x) for x in s2.split(","))


def process_lines(lines: list[str]) -> int:
    """
    >>> process_lines(TEST_INPUTS)
    21
    """
    return sum(count_arrangements(*parse(line)) for line in lines)


def main() -> int:
    lines = data.splitlines()
    result = process_lines(lines)
    return result


if __name__ == "__main__":
    print(main())
