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
    for y, line in enumerate(s.splitlines()):
        for x, c in enumerate(line):
            if c == "#":
                walls.add(Point(x, y))
            elif c in ".SE":
                if c == "S":
                    start = MazePoint(x, y, complex(1, 0))
                elif c == "E":
                    end = Point(x, y)

    # Find possible paths from start to end, and associated cost
    # (1 per step, 1000 per rotation)
    to_check = [(0, start)]
    paths = {start: []}  # The points that can reach this point
    costs = {start: 0}  # The cheapest way to get to this point
    while to_check:
        cost, curr = heapq.heappop(to_check)

        for next_cost, next_point in curr.neighbours(walls):
            new_cost = cost + next_cost
            if next_point not in costs or new_cost <= costs[next_point]:
                costs[next_point] = new_cost
                heapq.heappush(to_check, (new_cost, next_point))
                if next_point not in paths:
                    paths[next_point] = [(new_cost, curr)]
                else:
                    # We have reached this point before, potentially with
                    # a more expensive cost. Remove all ways to get here
                    # that are more expensive
                    new_paths = []
                    for c, p in paths[next_point] + [(new_cost, curr)]:
                        # We know that current method is cheapest, by costs
                        # dictionary check
                        if c == new_cost:
                            new_paths.append((c, p))
                    paths[next_point] = new_paths

    # The ways to reach the end
    ends = {mp: cost for mp, cost in costs.items() if mp.get_point() == end}
    # Restrict those to cheapest ones
    to_check = [mp for mp, cost in ends.items() if cost == min(ends.values())]
    seen = set(to_check)
    while to_check:
        # Work our way backwards through the paths
        curr = to_check.pop()
        next = set(n for _, n in paths.get(curr, []))
        if not next:
            continue
        for p in next:
            if p not in seen:
                to_check.append(p)
                seen.add(p)

    return len({mp.get_point() for mp in seen})


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
EXPECTED = 45

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
EXPECTED2 = 64


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
