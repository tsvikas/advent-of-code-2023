from aoc2023.common import Solution
from aoc2023.d15a import TEST_INPUT, hash_value


def follow_instructions(line: str) -> tuple[dict[int, list[str]], dict[str, int]]:
    """
    >>> box_to_order, label_to_len_power = follow_instructions(TEST_INPUT)
    >>> box_to_order[0]
    ['rn', 'cm']
    >>> box_to_order[3]
    ['ot', 'ab', 'pc']
    >>> label_to_len_power
    {'rn': 1, 'cm': 2, 'ot': 7, 'ab': 5, 'pc': 6}
    """
    box_to_order: dict[int, list[str]] = {i: [] for i in range(256)}
    label_to_len_power: dict[str, int] = {}
    for instruction in line.split(","):
        value: int | None
        if "-" in instruction:
            label = instruction.split("-")[0]
            value = None
        elif "=" in instruction:
            label, value_s = instruction.split("=")
            value = int(value_s)
        else:
            raise ValueError(f"Invalid instruction: {instruction!r}")
        box = hash_value(label)
        if value is None:
            if label in box_to_order[box]:
                box_to_order[box].remove(label)
                label_to_len_power.pop(label)
            else:
                assert label not in label_to_len_power
        else:
            if label not in box_to_order[box]:
                box_to_order[box].append(label)
            label_to_len_power[label] = value
    return box_to_order, label_to_len_power


def focusing_powers(
    box_to_order: dict[int, list[str]], label_to_len_power: dict[str, int]
) -> dict[str, int]:
    """
    >>> box_to_order, label_to_len_power = follow_instructions(TEST_INPUT)
    >>> focusing_powers(box_to_order, label_to_len_power)
    {'rn': 1, 'cm': 4, 'ot': 28, 'ab': 40, 'pc': 72}
    """
    return {
        label: (box + 1) * slot * label_to_len_power[label]
        for box, order in box_to_order.items()
        for slot, label in enumerate(order, 1)
    }


def process_lines(line: str) -> int:
    return sum(focusing_powers(*follow_instructions(line)).values())


solution = Solution.from_file(__file__, process_lines, {TEST_INPUT: 145})

if __name__ == "__main__":
    solution.submit()
