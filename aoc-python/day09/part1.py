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

    p1 = 0
    p2 = len(filesystem) - 1
    while True:
        if filesystem[p1] is not None:
            p1 += 1
            continue
        if filesystem[p2] is None:
            p2 -= 1
            continue
        if p1 >= p2:
            break
        filesystem[p1], filesystem[p2] = filesystem[p2], filesystem[p1]

    tot = 0
    for i, n in enumerate(filesystem):
        if n is not None:
            tot += i * n
    return tot

INPUT_S = '''\
2333133121414131402
'''
EXPECTED = 1928


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


INPUT_TXT = Path(__file__).parent / 'input.txt'


def main() -> int:
    with open(INPUT_TXT) as f, support.timing():
        print(compute(f.read()))

    return 1928


if __name__ == '__main__':
    raise SystemExit(main())
