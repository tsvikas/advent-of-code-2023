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


# ruff: noqa: FBT003
def count_arrangements(hot_springs: str, group_sizes: tuple[int, ...]) -> int:
    """
    >>> [count_arrangements(*parse(line)) for line in TEST_INPUTS]
    [1, 4, 1, 1, 4, 10]
    >>> [count_arrangements(*parse(line)) for line in TEST_INPUTS_2]
    [1, 506250]
    """

    @functools.cache
    def count_arrangements_(
        h_start: int, g_start: int, required_start_dot: bool  # noqa: FBT001
    ) -> int:
        assert g_start <= len(group_sizes)
        assert g_start == len(group_sizes) or group_sizes[g_start] > 0
        if len(hot_springs) < h_start:
            return 0
        if len(hot_springs) == h_start:
            if g_start < len(group_sizes):
                return 0
            return 1
        if (
            sum(group_sizes[g_start:]) + len(group_sizes) - g_start - 1
            > len(hot_springs) - h_start
        ):
            # not required, but speeds up the program
            return 0
        match hot_springs[h_start]:
            case ".":
                return count_arrangements_(h_start + 1, g_start, False)
            case "#":
                if required_start_dot:
                    return 0
                if not g_start < len(group_sizes):
                    return 0
                if "." in hot_springs[h_start + 1 : h_start + group_sizes[g_start]]:
                    return 0
                return count_arrangements_(
                    h_start + group_sizes[g_start], g_start + 1, True
                )
            case "?":
                # start with dot
                count = count_arrangements_(h_start + 1, g_start, False)
                # or start with hash
                if (
                    not required_start_dot
                    and g_start < len(group_sizes)
                    and "." not in hot_springs[h_start : h_start + group_sizes[g_start]]
                ):
                    count += count_arrangements_(
                        h_start + group_sizes[g_start], g_start + 1, True
                    )
                return count
        raise RuntimeError("unreachable")

    return count_arrangements_(0, 0, False)


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
    return process_lines(data.splitlines())


if __name__ == "__main__":
    print(main())
