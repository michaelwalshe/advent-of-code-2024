import math
from pathlib import Path


import pytest

import support


def compute(s: str) -> int:
    tot = 0
    for line in s.splitlines():
        ns = list(map(int, line.split()))
        for j in range(-1, len(ns)):
            if j != -1:
                n2s = ns.copy()
                n2s.pop(j)
            else:
                n2s = ns.copy()

            sign = 0
            for i in range(1, len(n2s)):
                delta = n2s[i] - n2s[i - 1]

                if delta == 0 or abs(delta) > 3:
                    break  # unsafe

                new_sign = math.copysign(1, delta)
                if sign != 0 and new_sign != sign:
                    break  # unsafe

                sign = new_sign

            else:  # nobreak
                tot += 1
                break
    return tot


INPUT_S = """\
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""
EXPECTED = 4


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, EXPECTED),),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


INPUT_TXT = Path(__file__).parent / "input.txt"


def main() -> int:
    with support.timing():
        print(compute(INPUT_S))

    with open(INPUT_TXT) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
