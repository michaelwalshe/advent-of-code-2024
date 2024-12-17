import heapq
from pathlib import Path
from typing import NamedTuple

import pytest

import support


class Point(NamedTuple):
    x: int
    y: int

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)

    def __lt__(self, other: "Point") -> bool:
        return self.x < other.x or (self.x == other.x and self.y < other.y)


class MazePoint(NamedTuple):
    x: int
    y: int
    dir: complex

    def get_point(self) -> Point:
        return Point(self.x, self.y)

    def rot90(self) -> "MazePoint":
        d2 = self.dir * 1j
        return MazePoint(self.x, self.y, d2)

    def rot270(self) -> "MazePoint":
        d2 = self.dir * -1j
        return MazePoint(self.x, self.y, d2)

    def neighbours(self, walls: set[Point]) -> list["MazePoint"]:
        rotations = [(1000, self.rot90()), (1000, self.rot270())]
        next_point = MazePoint(self.x + self.dir.real, self.y + self.dir.imag, self.dir)
        if next_point.get_point() in walls:
            return rotations
        return [(1, next_point)] + rotations

    def __lt__(self, other: "MazePoint") -> bool:
        return self.x < other.x or (self.x == other.x and self.y < other.y)


def compute(s: str) -> int:
    walls = set()
    empty = set()
    for y, line in enumerate(s.splitlines()):
        for x, c in enumerate(line):
            if c == "#":
                walls.add(Point(x, y))
            elif c in ".SE":
                empty.add(Point(x, y))
                if c == "S":
                    start = MazePoint(x, y, complex(1, 0))
                elif c == "E":
                    end = Point(x, y)

    # Find possible paths form start to end, and associated cost
    # (1 per step, 1000 per rotation)
    to_check = [(0, start)]
    paths = {start: None}
    costs = {start: 0}
    while to_check:
        cost, curr = heapq.heappop(to_check)

        if curr.get_point() == end:
            break

        for next_cost, next_point in curr.neighbours(walls):
            new_cost = cost + next_cost
            if next_point not in costs or new_cost < costs[next_point]:
                costs[next_point] = new_cost
                heapq.heappush(to_check, (new_cost, next_point))
                paths[next_point] = curr

    # curr = end
    # path = []
    # tot_cost = 0
    # while curr != start:
    #     path.append(curr)
    #     curr = paths[curr]
    #     tot_cost += 1

    return cost


INPUT_S = """\
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
"""
EXPECTED = 7036

INPUT_S2 = """\
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
"""
EXPECTED2 = 11048


@pytest.mark.parametrize(
    ("input_s", "expected"),
    (
        (INPUT_S, EXPECTED),
        (INPUT_S2, EXPECTED2),
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
