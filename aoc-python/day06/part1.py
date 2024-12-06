from pathlib import Path

import pytest

import support


def compute(s: str) -> int:
    obstacles: set[complex] = set()
    guard_path: list[complex] = []
    max_j = len(s.splitlines())
    max_i = len(s.splitlines()[0])
    for j, line in enumerate(s.splitlines()):
        for i, c in enumerate(line):
            if c == "#":
                obstacles.add(complex(i, j))
            elif c == "^":
                guard_path.append(complex(i, j))

    di_dj = complex(0, -1)

    while True:
        # Get current guard position
        guard = guard_path[-1]

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
        guard_path.append(next_guard)

    return len(set(guard_path))


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
EXPECTED = 41


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
