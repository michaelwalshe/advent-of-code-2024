from pathlib import Path

import pytest

import support

from functools import cache


def compute(s: str) -> int:
    towels_s, designs_s = s.strip().split("\n\n")
    towels = set(towels_s.split(", "))
    designs = designs_s.split("\n")

    @cache
    def dfs(design: str) -> int:
        #  Perform recursive DFS to find all possible ways to fold the towel
        #  to match the design.
        if not design:
            return 1
        npossible = 0
        for i in range(1, len(design) + 1):
            if design[:i] in towels:
                npossible += dfs(design[i:])
        return npossible

    npossible = 0
    for design in designs:
        npossible += dfs(design)

    return npossible


INPUT_S = """\
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
"""
EXPECTED = 16


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
