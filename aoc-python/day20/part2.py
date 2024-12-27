import heapq
from collections import deque
from itertools import combinations
from pathlib import Path
from typing import Generator, NamedTuple

import pytest

import support


class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Point") -> "Point":
        return Point(self.x - other.x, self.y - other.y)

    def __eq__(self, other: "Point") -> bool:
        return self.x == other.x and self.y == other.y

    def __lt__(self, other: "Point") -> bool:
        return self.x < other.x or self.y < other.y


type AdjacencyGraph = dict[Point, list[tuple[Point, int]]]

DIRECTIONS = [Point(0, -1), Point(1, 0), Point(0, 1), Point(-1, 0)]


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


def neighbours(
    p: Point, walls: set[Point], max_i: Point, max_j: Point
) -> Generator[Point, None, None]:
    for d in DIRECTIONS:
        n = p + d
        if n not in walls and 0 <= n.x <= max_i and 0 <= n.y <= max_j:
            yield n


def compute(s: str, time_save: int = 100) -> int:
    walls: set[Point] = set()
    for j, line in enumerate(s.strip().splitlines()):
        for i, c in enumerate(line):
            if c == "#":
                walls.add(Point(i, j))
            elif c == "S":
                start = Point(i, j)
            elif c == "E":
                end = Point(i, j)
    max_i = max(walls, key=lambda p: p.x).x
    max_j = max(walls, key=lambda p: p.y).y

    distances = {start: 0}
    to_check = [start]
    while to_check:
        p = to_check.pop()
        for n in neighbours(p, walls, max_i, max_j):
            if n not in distances:
                distances[n] = distances[p] + 1
                to_check.append(n)

    tot = 0
    for (p, i), (q, j) in combinations(distances.items(), 2):
        d = abs(p.x - q.x) + abs(p.y - q.y)
        if d <= 20 and j - i - d >= time_save:
            tot += 1

    return tot


INPUT_S = """\
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
"""
EXPECTED = 5


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, EXPECTED),),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s, 20) == expected


INPUT_TXT = Path(__file__).parent / "input.txt"


def main() -> int:
    print(compute(INPUT_S, 20))

    with open(INPUT_TXT) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
