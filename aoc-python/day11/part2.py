from functools import cache
from math import log10
from pathlib import Path

import pytest

import support


@cache
def count_transformed_stones(nums: tuple[int, ...], n_blinks: int) -> int:
    if n_blinks == 0:
        return len(nums)

    count = 0
    for n in nums:
        if n == 0:
            next_n = (1,)
        else:
            n_digits = int(log10(n)) + 1

            if n_digits % 2 == 0:
                n_str = str(n)
                next_n = (int(n_str[0 : n_digits // 2]), int(n_str[n_digits // 2 :]))
            else:
                next_n = (n * 2024,)
        count += count_transformed_stones(next_n, n_blinks - 1)
    return count


def compute(s: str, n_blinks: int = 75) -> int:
    numbers = tuple(support.parse_numbers_split(s))

    return count_transformed_stones(numbers, n_blinks)


INPUT_S = """\
125 17
"""
EXPECTED = 55312


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, EXPECTED),),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s, 25) == expected


INPUT_TXT = Path(__file__).parent / "input.txt"


def main() -> int:
    print(compute(INPUT_S, 25))

    with open(INPUT_TXT) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
