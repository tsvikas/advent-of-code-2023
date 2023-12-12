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


def count_arrangements(  # noqa: C901
    hot_springs: str, group_sizes: tuple[int, ...]
) -> int:
    """
    >>> [count_arrangements(*parse(line)) for line in TEST_INPUTS]
    [1, 4, 1, 1, 4, 10]
    >>> [count_arrangements(*parse(line)) for line in TEST_INPUTS_2]
    [1, 506250]
    """

    @functools.cache
    def count_arrangements_(  # noqa: C901, PLR0911
        start: int, group_sizes: tuple[int, ...], required_start: str
    ) -> int:
        assert required_start in {"", ".", "#"}
        assert not group_sizes or group_sizes[0] > 0
        if len(hot_springs) == start:
            if group_sizes:
                return 0
            assert required_start != "#"
            return 1
        if sum(group_sizes) + len(group_sizes) - 1 > len(hot_springs) - start:
            # not required, but speeds up the program
            return 0
        match hot_springs[start]:
            case ".":
                if required_start == "#":
                    return 0
                return count_arrangements_(start + 1, group_sizes, "")
            case "#":
                if required_start == ".":
                    return 0
                if not group_sizes:
                    return 0
                if "." in hot_springs[start + 1 : start + group_sizes[0]]:
                    return 0
                return count_arrangements_(start + group_sizes[0], group_sizes[1:], ".")
            case "?":
                count = 0
                if required_start in {".", ""}:
                    count += count_arrangements_(start + 1, group_sizes, "")
                if (
                    required_start in {"#", ""}
                    and group_sizes
                    and "." not in hot_springs[start : start + group_sizes[0]]
                ):
                    count += count_arrangements_(
                        start + group_sizes[0], group_sizes[1:], "."
                    )
                return count
        raise RuntimeError("unreachable")

    return count_arrangements_(0, group_sizes, "")


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
