from itertools import product
import math as m
from pathlib import Path
import re
import pytest

import support


def print_grid(points, max_x, max_y):
    grid = [["." for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    for x, y in points:
        grid[y][x] = "#"
    for row in grid:
        print("".join(row))


def move_robot(x, y, vx, vy, max_x, max_y, seconds):
    for _ in range(seconds):
        x2 = x + vx
        y2 = y + vy
        if x2 < 0:
            x2 = max_x + x2 + 1
        elif x2 > max_x:
            x2 = x2 - max_x - 1
        if y2 < 0:
            y2 = max_y + y2 + 1
        elif y2 > max_y:
            y2 = y2 - max_y - 1
        x = x2
        y = y2
    return x, y


def compute(s: str, max_x=10, max_y=7) -> int:
    robots = []
    for line in s.splitlines():
        x, y, vx, vy = map(int, re.findall(r"-?\d+", line))
        robots.append((x, y, vx, vy))

    new_robots = []
    for x, y, vx, vy in robots:
        new_robots.append(move_robot(x, y, vx, vy, max_x, max_y, 100))

    print(print_grid([(x, y) for x, y, *_ in new_robots], max_x, max_y))

    # Count robots in each quadrant
    counts = [0, 0, 0, 0]
    for x, y, *_ in new_robots:
        if x < max_x // 2:
            if y < max_y // 2:
                counts[0] += 1
            elif y > max_y // 2:
                counts[1] += 1
        elif x > max_x // 2:
            if y < max_y // 2:
                counts[2] += 1
            elif y > max_y // 2:
                counts[3] += 1

    return m.prod(counts)


INPUT_S = """\
p=2,4 v=2,-3
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=9,5 v=-3,-3
"""
EXPECTED = 12


@pytest.mark.parametrize(
    ("input_s", "expected", "max_x", "max_y"),
    ((INPUT_S, EXPECTED, 10, 6),),
)
def test(input_s: str, expected: int, max_x: int, max_y: int) -> None:
    assert compute(input_s, max_x, max_y) == expected


INPUT_TXT = Path(__file__).parent / "input.txt"


def main() -> int:
    print(compute(INPUT_S, 10, 6))

    with open(INPUT_TXT) as f, support.timing():
        print(compute(f.read(), 100, 102))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
