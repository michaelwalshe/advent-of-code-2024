from collections import deque
from pathlib import Path
from typing import Generator, NamedTuple

import pytest

import support


class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)

    def __eq__(self, other: "Point") -> bool:
        return self.x == other.x and self.y == other.y


def print_grid(points, max_x, max_y):
    grid = [["." for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    for x, y in points:
        grid[y][x] = "#"
    for row in grid:
        print("".join(row))


def print_path(path, points, max_x, max_y):
    grid = [["." for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    for x, y in points:
        grid[y][x] = "#"
    for x, y in path:
        assert grid[y][x] != "#"
        grid[y][x] = "O"
    for row in grid:
        print("".join(row))


def compute(s: str, bytes: int = 12, max_x: int = 6, max_y: int = 6) -> int:
    corrupt = set()
    for i, line in enumerate(s.splitlines()):
        p = Point(*map(int, line.split(",")))
        corrupt.add(p)
        if i == bytes - 1:
            break

    start = Point(0, 0)
    end = Point(max_x, max_y)

    def neighbors(p: Point) -> Generator[Point]:
        for d in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            np = p + Point(*d)
            if 0 <= np.x <= max_x and 0 <= np.y <= max_y and np not in corrupt:
                yield np
        return []

    print_grid(corrupt, max_x, max_y)

    def bfs() -> Generator[list[Point]]:
        queue = deque([(start, [start])])
        visited = set()
        while queue:
            (p, path) = queue.popleft()
            for np in neighbors(p):
                if np == end:
                    yield path + [np]
                if np in visited:
                    continue
                visited.add(np)
                queue.append((np, path + [np]))

    paths = list(bfs())

    print_path(paths[0], corrupt, max_x, max_y)
    return len(paths[0]) - 1


INPUT_S = """\
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
"""
EXPECTED = 22


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
        print(compute(f.read(), 1024, 70, 70))

    return 22


if __name__ == "__main__":
    raise SystemExit(main())
