from pathlib import Path
from typing import Iterable

import pytest

import support


def find_neighbouring_plots(
    i: int, j: int, grid: dict[tuple[int, int], str]
) -> list[tuple[int, int]]:
    # Perform a BFS to find all cells in grid that have the same value as the cell at (i, j)
    # and are connected to it via a path of cells with the same value.
    c = grid[(i, j)]
    queue = [(i, j)]
    neighbours = {(i, j)}
    visited = set()
    while queue:
        i, j = queue.pop()
        visited.add((i, j))
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            i_di, j_dj = i + di, j + dj
            if (
                (i_di, j_dj) not in visited
                and (i_di, j_dj) in grid
                and grid[(i_di, j_dj)] == c
            ):
                queue.append((i_di, j_dj))
                neighbours.add((i_di, j_dj))
    return neighbours


def compute(s: str) -> int:
    grid: dict[tuple[int, int], str] = {}
    for j, row in enumerate(s.splitlines()):
        for i, c in enumerate(row):
            grid[(i, j)] = c

    regions: dict[tuple[str, int], set[tuple[int, int]]] = {}

    visited_cells = set()
    region_i_di = 0
    for p, c in grid.items():
        if p in visited_cells:
            continue
        regions[(region_i_di, c)] = find_neighbouring_plots(p[0], p[1], grid)
        visited_cells.update(regions[(region_i_di, c)])
        region_i_di += 1

    # Now determine the perimeter of each region. Find out for each
    # cell how many of its neighbours are not in the same region (or not in the grid).
    # The sum of these values is the perimeter of the region.
    perimeters = {}
    for region, cells in regions.items():
        perimeter = 0
        for cell in cells:
            i, j = cell
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                i_di, j_dj = i + di, j + dj
                if (i_di, j_dj) not in cells:
                    perimeter += 1
        perimeters[region] = perimeter

    # Final total, result of summing up perimiter * area for each region.
    return sum(len(cells) * perimeters[region] for region, cells in regions.items())


INPUT_S = """\
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
"""
EXPECTED = 1930


@pytest.mark.parametrize(
    ("input_s", "eipected"),
    ((INPUT_S, EXPECTED),),
)
def test(input_s: str, eipected: int) -> None:
    assert compute(input_s) == eipected


INPUT_TXT = Path(__file__).parent / "input.txt"


def main() -> int:
    print(compute(INPUT_S))

    with open(INPUT_TXT) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
