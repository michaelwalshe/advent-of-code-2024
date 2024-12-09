import itertools
from pathlib import Path

import pytest

import support

operators = {
    "+": lambda a, b: a + b,
    "*": lambda a, b: a * b,
    "||": lambda a, b: int(str(a) + str(b)),
}


def compute(s: str) -> int:
    possible_results = []
    for line in s.splitlines():
        out_s, nums_s = line.split(": ")
        nums = [int(n) for n in nums_s.split()]
        out = int(out_s)

        for operator_choices in itertools.product(
            operators.keys(), repeat=len(nums) - 1
        ):
            res = nums[0]
            for num, op in zip(nums[1:], operator_choices):
                res = operators[op](res, num)
            if res == out:
                possible_results.append(out)
                break
    return sum(possible_results)


INPUT_S = """\
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""
EXPECTED = 11387


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
