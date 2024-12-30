from pathlib import Path

import pytest

import support


def next_number(n: int) -> int:
    n = n ^ (n * 64)
    n = n % 16777216
    n = n ^ (n // 32)
    n = n % 16777216
    n = n ^ (n * 2048)
    n = n % 16777216
    return n


def compute(s: str) -> int:
    start_numbers = [int(line) for line in s.splitlines()]

    tot = 0
    for n in start_numbers:
        for _ in range(2000):
            n = next_number(n)
        tot += n

    return tot


INPUT_S = """\
1
10
100
2024
"""
EXPECTED = 37327623


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

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
