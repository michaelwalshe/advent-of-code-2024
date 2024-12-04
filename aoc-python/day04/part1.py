from pathlib import Path

import pytest

import support


def check_bounds(grid, x, y):
    return 0 <= y < len(grid) and 0 <= x < len(grid[0])


def get_neighbour_xmas(grid, x, y):
    neighbour_xmas = 0
    # Get horizontal, vertical, and diagonal neighbouring
    # cells of current cell, for the next 3 cells
    for dir in (-1, 1):
        for dx, dy in [(0, 1), (1, 0), (1, 1), (-1, 1)]:
            dx = dir * dx
            dy = dir * dy
            word = grid[y][x]
            for i in range(dir, dir * 4):
                x2 = x + i * dx
                y2 = y + i * dy
                if check_bounds(grid, x2, y2):
                    word = word + grid[y2][x2]
                if word == 'XMAS' or word == 'SAMX':
                    neighbour_xmas += 1
    return neighbour_xmas


def compute(s: str) -> int:
    grid = [s for s in s.split('\n') if s]

    count = 0
    for j in range(len(grid)):
        for i in range(len(grid[0])):
            count += get_neighbour_xmas(grid, i, j)

    return count


INPUT_S = '''\
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
'''
EXPECTED = 18


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
