from pathlib import Path
from itertools import product
import re

import pytest

import support


def compute(s: str) -> int:
    mul_do_pat = re.compile(
        r"""
        (?P<mul>mul\((\d+),(\d+)\))  # Fetch all mul(int1, int2) groups
        | (?P<do>do\(\))  # Match the do() group
        | (?P<dont>don\'t\(\))  # Match the don't() group
        """,
        re.VERBOSE,
    )
    res = 0
    doing = True
    for m in re.finditer(mul_do_pat, s):
        if doing and m.group("mul"):
            res += int(m.group(2)) * int(m.group(3))
        elif m.group("do"):
            doing = True
        elif m.group("dont"):
            doing = False
    return res


INPUT_S = """\
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
"""
EXPECTED = 48


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, EXPECTED),),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


INPUT_TXT = Path(__file__).parent / "input.txt"


def main() -> int:
    with open(INPUT_TXT) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
