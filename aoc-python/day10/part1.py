from pathlib import Path
from typing import Generator

import pytest

import support


def safe_int(s: str) -> int:
    try:
        return int(s)
    except ValueError:
        return 999


def compute(s: str) -> int:
    grid = [list(map(safe_int, line)) for line in s.splitlines()]
    max_j = len(grid) - 1
    max_i = len(grid[0]) - 1

    def get_next(i: int, j: int) -> Generator[tuple[int, int], None, None]:
        cur_point = grid[j][i]
        for di, dj in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            next_i, next_j = i + di, j + dj
            if (
                0 <= next_i <= max_i
                and 0 <= next_j <= max_j
                and grid[next_j][next_i] == cur_point + 1
            ):
                yield next_i, next_j

    # Find all 0s and 9s
    zeros = set()
    nines = set()
    for j, row in enumerate(grid):
        for i, point in enumerate(row):
            if point == 0:
                zeros.add((i, j))
            elif point == 9:
                nines.add((i, j))

    # Find all paths from each 0 to any 9
    # Not storing the full path, just the 9 it could
    # reach from the 0
    paths = {}
    for i, j in zeros:
        paths[(i, j)] = []
        stack = [(i, j)]
        while stack:
            cur_i, cur_j = stack.pop()
            for next_i, next_j in get_next(cur_i, cur_j):
                if (next_i, next_j) in nines:
                    paths[(i, j)].append((next_i, next_j))
                else:
                    stack.append((next_i, next_j))
    return sum(len(set(v)) for v in paths.values())


INPUT_S_1 = """\
10..9..
2...8..
3...7..
4567654
...8..3
...9..2
.....01
"""

INPUT_S = """\
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""
EXPECTED = 36


@pytest.mark.parametrize(
    ("input_s", "expected"),
    (
        (INPUT_S_1, 3),
        (INPUT_S, EXPECTED),
    ),
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
