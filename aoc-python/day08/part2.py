import itertools
from pathlib import Path

import pytest

import support


def compute(s: str) -> int:
    grid = s.strip().splitlines()
    max_i = len(grid[0]) - 1
    max_j = len(grid) - 1

    antennas = {}
    for j, row in enumerate(grid):
        for i, cell in enumerate(row):
            if cell != '.':
                if cell not in antennas:
                    antennas[cell] = [(i, j)]
                else:
                    antennas[cell].append((i, j))

    antinodes = set()
    for posns in antennas.values():
        for p1, p2 in itertools.combinations(posns, 2):
            di, dj = p2[0] - p1[0], p2[1] - p1[1]
            a1 = (p1[0] - di, p1[1] - dj)
            a2 = (p2[0] + di, p2[1] + dj)
            while a1[0] >= 0 and a1[0] <= max_i and a1[1] >= 0 and a1[1] <= max_j:
                antinodes.add(a1)
                a1 = (a1[0] - di, a1[1] - dj)
            while a2[0] >= 0 and a2[0] <= max_i and a2[1] >= 0 and a2[1] <= max_j:
                antinodes.add(a2)
                a2 = (a2[0] + di, a2[1] + dj)
            antinodes.add(p1)
            antinodes.add(p2)

    return len(antinodes)


INPUT_S = '''\
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
'''
EXPECTED = 34


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


INPUT_TXT = Path(__file__).parent / 'input.txt'


def main() -> int:
    with open(INPUT_TXT) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
