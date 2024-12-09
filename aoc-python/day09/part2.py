import collections
from pathlib import Path

import pytest

import support


def compute(s: str) -> int:
    numbers = [int(c) for c in s.strip()]
    filesystem = []

    is_file = True
    i = 0
    for n in numbers:
        if is_file:
            for _ in range(n):
                filesystem.append(i)
            i += 1
        else:
            for _ in range(n):
                filesystem.append(None)
        is_file = not is_file

    # Setup free space pointers
    def get_next_free_space(i: int) -> tuple[int, int]:
        # Search for next None value, and the end of the Nones
        # Will raise ValueError if no more free space
        p1_2 = p1_1 = filesystem.index(None, i)
        while p1_2 < len(filesystem) and filesystem[p1_2] is None:
            p1_2 += 1
        return p1_1, p1_2

    p1_1, p1_2 = get_next_free_space(0)

    # Setup file pointers
    def get_file(file_index: int) -> tuple[int, int]:
        # Return the start and end of the file with that index
        p2_2 = p2_1 = filesystem.index(file_index)
        while p2_2 < len(filesystem) and filesystem[p2_1] == filesystem[p2_2]:
            p2_2 += 1
        return p2_1, p2_2

    file_idx = max(f for f in filesystem if f is not None)
    p2_1, p2_2 = get_file(file_idx)

    # [1, 4, ., ., ., 2, 2, ., 3, 3, 3, 3, ., ., ., .]
    #        ^        ^        ^           ^
    #        p1_1     p1_2     p2_1        p2_2
    while True:
        # If the current file fits in the free space and we're
        # not checking free space to the right of the file
        if p1_2 <= p2_1 and p1_2 - p1_1 >= p2_2 - p2_1:
            # Move the file
            (
                filesystem[p1_1 : (p1_1 + (p2_2 - p2_1))],
                filesystem[p2_1:p2_2]
            ) = (
                filesystem[p2_1:p2_2],
                filesystem[p1_1 : (p1_1 + (p2_2 - p2_1))],
            )
        else:
            # This file doesn't fit, so check next free space
            try:
                p1_1, p1_2 = get_next_free_space(p1_2)
                if p1_2 <= p2_1:
                    continue
            except ValueError:
                # If no more free space, then need to check a new file
                pass

        # Move to next file
        file_idx -= 1
        if file_idx < 0:
            # If no more files, then we are done
            break

        # Reset our pointers
        p2_1, p2_2 = get_file(file_idx)
        try:
            p1_1, p1_2 = get_next_free_space(0)
        except ValueError:
            # If no more free space, then we are done
            break

    tot = 0
    for i, n in enumerate(filesystem):
        if n is not None:
            tot += i * n
    return tot


INPUT_S = """\
2333133121414131402
"""
EXPECTED = 2858


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, EXPECTED),),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


INPUT_TXT = Path(__file__).parent / "input.txt"


def main() -> int:
    print(compute(INPUT_S))
    with open(INPUT_TXT) as f, support.timing():
        print(compute(f.read()))

    return 1928


if __name__ == "__main__":
    raise SystemExit(main())
