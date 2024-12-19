from pathlib import Path

import pytest

import support

from collections import deque

def compute(s: str) -> int:
    towels_s, designs_s = s.strip().split("\n\n")
    towels = set(towels_s.split(", "))
    designs = designs_s.split("\n")

    def dfs(design: str) -> list[str]:
        #  Perform DFS to find if design can be made from towels
        queue = [(0, [])]
        while queue:
            left, path = queue.pop()
            if left == len(design):
                return path
            for right in range(left + 1, len(design) + 1):
                towel = design[left:right]
                if towel in towels:
                    queue.append((right, path + [towel]))
        return []

    npossible = 0
    for design in designs:
        towel_path = dfs(design)
        if towel_path and "".join(towel_path) == design:
            npossible += 1

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
EXPECTED = 6


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
