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
def count_arrangement(  # noqa: PLR0911
    record: str, damaged: tuple[int, ...], *, start: str = ""
) -> int:
    """
    >>> [count_arrangement(*parse(line)) for line in TEST_INPUTS]
    [1, 4, 1, 1, 4, 10]
    >>> [count_arrangement(*parse(line)) for line in TEST_INPUTS_2]
    [1, 506250]
    """
    if not record:
        return 1 if not damaged else 0
    match record[0]:
        case ".":
            if start == "#":
                return 0
            assert start in {"", "."}
            return count_arrangement(record[1:], damaged, start="")
        case "#":
            if start == ".":
                return 0
            if not damaged:
                return 0
            if damaged[0] == 0:
                return 0
            if damaged[0] == 1:
                return count_arrangement(record[1:], damaged[1:], start=".")
            assert damaged[0] > 1
            new_damaged = (damaged[0] - 1, *damaged[1:])
            return count_arrangement(record[1:], new_damaged, start="#")
        case "?":
            return count_arrangement(
                "." + record[1:], damaged, start=start
            ) + count_arrangement("#" + record[1:], damaged, start=start)
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
    return sum(count_arrangement(*parse(line)) for line in lines)


def main() -> int:
    lines = data.splitlines()
    result = process_lines(lines)
    return result


if __name__ == "__main__":
    print(main())
