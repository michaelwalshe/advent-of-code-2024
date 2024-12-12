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
                neighbours.add((i_di, j_dj))  # We double count some but cba fixing
    return neighbours


def compute(s: str) -> int:
    grid: dict[tuple[int, int], str] = {}
    for j, row in enumerate(s.splitlines()):
        for i, c in enumerate(row):
            grid[(i, j)] = c

    regions: dict[tuple[str, int], set[tuple[int, int]]] = {}

    visited_cells = set()
    region_idx = 0
    for p, c in grid.items():
        if p in visited_cells:
            continue
        regions[(region_idx, c)] = find_neighbouring_plots(p[0], p[1], grid)
        visited_cells.update(regions[(region_idx, c)])
        region_idx += 1

    # Now determine how many sides each region has. This is basically
    # for each cell in the region, check if any of its neighbours are not in the region.
    # Then, that cell is on a side. Now check if we have already counted that side. If
    # not, then  move orthoganally to the direction that was not in the region and check
    # if that cell is in the region and is still on the side in the same direction as
    # before.  If so, then this is still on that side, keep moving till we reach a
    # corner. Do the same in the other direction and we should have added all cells
    # and the direction of the side to the set of sides for this region

    sides: dict[tuple[str, int], int] = {}
    for region, cells in regions.items():
        sides[region] = 0
        # For sides, keep track of cell on the edge, plus direction to leave the region
        seen_sides = set()
        for i, j in cells:
            for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                if (i + di, j + dj) in cells:
                    continue
                # This is a side! Check if we have seen it before
                if (i, j, di, dj) in seen_sides:
                    continue
                # New side, so increment the count
                sides[region] += 1
                seen_sides.add((i, j, di, dj))
                # Now move orthoganally to the direction that was not in the region
                if di != 0:
                    di2, dj2 = 0, 1
                else:  # dj != 0
                    di2, dj2 = 1, 0
                # Add all other cells on this side to seen_sides, so we dont count
                # this side again
                for dir in (1, -1):
                    n = dir
                    while (i + n * di2, j + n * dj2) in cells and (
                        i + di + n * di2,
                        j + dj + n * dj2,
                    ) not in cells:
                        seen_sides.add((i + n * di2, j + n * dj2, di, dj))
                        n += dir

    # Final total, result of summing up perimiter * area for each region.
    return sum(len(cells) * sides[region] for region, cells in regions.items())


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
EXPECTED = 1206


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
