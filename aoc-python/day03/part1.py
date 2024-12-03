from pathlib import Path
from itertools import product
import re

import pytest

import support


def compute(s: str) -> int:
    mul_pat = re.compile(r"mul\((\d+),(\d+)\)")
    muls = mul_pat.findall(s)
    res = 0
    for a, b in muls:
        res += int(a) * int(b)
    return res


INPUT_S = '''\
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
'''
EXPECTED = 161


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
