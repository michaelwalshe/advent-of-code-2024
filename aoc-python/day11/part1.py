from functools import cache
from math import log10
from pathlib import Path

import pytest

import support


@cache
def transform_stone(n: int) -> tuple[int, ...]:
    if n == 0:
        return (1,)

    n_digits = int(log10(n)) + 1

    if n_digits % 2 == 0:
        n_str = str(n)
        return int(n_str[0 : n_digits // 2]), int(n_str[n_digits // 2 :])

    return (n * 2024,)


def compute(s: str, n_blinks: int = 25) -> int:
    numbers = support.parse_numbers_split(s)

    for _ in range(n_blinks):
        new_numbers = []
        for n in numbers:
            new_numbers.extend(transform_stone(n))
        numbers = new_numbers

    return len(numbers)


INPUT_S = """\
125 17
"""
EXPECTED = 55312


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
