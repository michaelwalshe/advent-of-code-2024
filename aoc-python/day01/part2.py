from pathlib import Path

import pytest

import support

from collections import Counter


def compute(s: str) -> int:
    n1s, n2s = [], []
    lines = s.splitlines()
    for line in lines:
        n1, n2 = map(int, line.split())
        n1s.append(n1)
        n2s.append(n2)

    n2_counts = Counter(n2s)

    tot = 0
    for n1 in n1s:
        tot += n2_counts[n1] * n1

    return tot


INPUT_S = '''\
3   4
4   3
2   5
1   3
3   9
3   3
'''
EXPECTED = 31


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

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
