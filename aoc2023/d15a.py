from aoc2023.common import Solution

TEST_INPUT = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"


def hash_value(instruction: str) -> int:
    """
    >>> [hash_value(instruction) for instruction in TEST_INPUT.split(',')]
    [30, 253, 97, 47, 14, 180, 9, 197, 48, 214, 231]
    """
    value = 0
    for c in instruction:
        value += ord(c)
        value *= 17
        value %= 256
    return value


def process_lines(line: str) -> int:
    return sum(hash_value(instruction) for instruction in line.split(","))


solution = Solution.from_file(__file__, process_lines, {TEST_INPUT: 1320})

if __name__ == "__main__":
    solution.test_inputs()
    solution.submit()
