from pathlib import Path

import pytest

import support


def print_map(path, obstacles, max_i, max_j):
    map = ""
    for j in range(max_j):
        for i in range(max_i):
            if complex(i, j) in path:
                map += "X"
            elif complex(i, j) in obstacles:
                map += "#"
            else:
                map += "."
        map += "\n"
    print(map)


def check_loop(
    guard_start: complex, obstacles: set[complex], max_i: int, max_j: int
) -> tuple[bool, set[tuple[complex, complex]]]:
    di_dj = complex(0, -1)
    guard = guard_start

    guard_path: set[tuple[complex, complex]] = {(guard, di_dj)}

    while True:
        # Check next position for an obstacle
        next_guard = guard + di_dj
        if (
            next_guard.real < 0
            or next_guard.imag < 0
            or next_guard.real >= max_i
            or next_guard.imag >= max_j
        ):
            # We're done!
            break
        if next_guard in obstacles:
            # Rotate to the right
            di_dj = di_dj * complex(0, 1)
            # Try and move again!
            continue
        # Otherwise, we've succeeded, try and move
        if (next_guard, di_dj) in guard_path:
            # We've been here before, with this direction. This is a loop!
            # print("Loop detected...")
            # print_map([posn for posn, _ in guard_path], obstacles, max_i, max_j)
            return True, guard_path

        guard = next_guard
        guard_path.add((guard, di_dj))

    return False, guard_path


def compute(s: str) -> int:
    obstacles: set[complex] = set()
    max_j = len(s.splitlines())
    max_i = len(s.splitlines()[0])
    for j, line in enumerate(s.splitlines()):
        for i, c in enumerate(line):
            if c == "#":
                obstacles.add(complex(i, j))
            elif c == "^":
                guard_start = complex(i, j)

    initial_path = check_loop(guard_start, obstacles, max_i, max_j)[1]

    # New obstacles should be somewhere in that loop - get just
    # the unique i, j ignoring dirs
    possible_posns = []
    for posn in set(p for p, _ in initial_path) - {guard_start}:
        if check_loop(guard_start, obstacles | {posn}, max_i, max_j)[0]:
            possible_posns.append(posn)

    return len(possible_posns)


INPUT_S = """\
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""
EXPECTED = 6


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
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
