from pathlib import Path

import pytest

import support


def check_bounds(grid: list[str], x: int, y: int) -> bool:
    return 0 <= y < len(grid) and 0 <= x < len(grid[0])


def check_neighbour_xmas(grid: list[str], x: int, y: int) -> bool:
    for dir in (-1, 1):
        mas = grid[y][x]
        for dx, dy in ((-1, -1), (1, 1)):
            x2 = x + dir * dx
            y2 = y + dy
            if check_bounds(grid, x2, y2):
                mas += grid[y2][x2]
        if set(mas) != {"M", "A", "S"}:
            return False
    else:
        return True


def compute(s: str) -> int:
    grid = [s for s in s.split("\n") if s]

    count = 0
    for j in range(len(grid)):
        for i in range(len(grid[0])):
            if grid[j][i] == 'A' and check_neighbour_xmas(grid, i, j):
                count += 1

    return count


INPUT_S = """\
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
"""
EXPECTED = 9


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, EXPECTED),),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


INPUT_TXT = Path(__file__).parent / "input.txt"


def main() -> int:
    with open(INPUT_TXT) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
