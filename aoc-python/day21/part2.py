from collections import deque
from dataclasses import dataclass
from functools import cache
from pathlib import Path

import pytest

import support

"""
+---+---+---+
| 7 | 8 | 9 |
+---+---+---+
| 4 | 5 | 6 |
+---+---+---+
| 1 | 2 | 3 |
+---+---+---+
    | 0 | A |
    +---+---+
"""

"""
    +---+---+
    | ^ | A |
+---+---+---+
| < | v | > |
+---+---+---+
"""

NUMERIC_KEYPAD = {
    0 + 0j: "7",
    0 + 1j: "8",
    0 + 2j: "9",
    1 + 0j: "4",
    1 + 1j: "5",
    1 + 2j: "6",
    2 + 0j: "1",
    2 + 1j: "2",
    2 + 2j: "3",
    3 + 1j: "0",
    3 + 2j: "A",
}

DIRECTION_KEYPAD = {0 + 1j: "^", 0 + 2j: "A", 1 + 0j: "<", 1 + 1j: "v", 1 + 2j: ">"}

DIR2MOVE = {"^": -1 + 0j, "v": 1 + 0j, "<": 0 - 1j, ">": (0 + 1j)}


def move_robot(p: complex, dir: str, robo_type: str) -> complex | None:
    p2 = p + DIR2MOVE[dir]
    check_dict = NUMERIC_KEYPAD if robo_type == "N" else DIRECTION_KEYPAD
    if p2 in check_dict:
        return p2
    else:
        return None


@cache
def neighbours(
    rd_posns: tuple[complex, ...], rn: complex
) -> list[tuple[str, str, tuple[complex, ...], complex]]:
    # Return the next possible states from the current state
    states = []
    for my_move in "A^<v>":
        code_next = ""
        rn_next = rn
        rd_next = list(rd_posns)
        # For each next button we can press, check what that would
        # do to the rest of the robots
        # If an A is pressed, that triggers checking the next level of
        # robots
        if my_move == "A":
            i = 0
            while i < len(rd_posns) - 1:
                move = DIRECTION_KEYPAD[rd_posns[i]]
                if move == "A":
                    i += 1
                else:
                    rd_next[i + 1] = move_robot(rd_posns[i + 1], move, "D")
                    break
            else:  # nobreak
                if DIRECTION_KEYPAD[rd_posns[-1]] == "A":
                    code_next = NUMERIC_KEYPAD[rn]
                else:
                    rn_next = move_robot(rn, DIRECTION_KEYPAD[rd_posns[-1]], "N")
        else:
            rd_next[0] = move_robot(rd_posns[0], my_move, "D")

        if (all(r is not None for r in rd_next) and rn_next is not None) and (
            code_next != ""
            or any(r1 != r2 for r1, r2 in zip(rd_posns, rd_next))
            or rn != rn_next
        ):
            states.append((code_next, tuple(rd_next), rn_next))

    return states


@cache
def bfs(code: str, rd_posns: tuple[complex, ...], rn: complex) -> str:
    if len(code) == 1:
        visited = {("", rd_posns, rn)}
        queue = deque([("", 0, rd_posns, rn)])

        while queue:
            cur_code, pathlen, rd_posns, rn = queue.popleft()

            if cur_code == code:
                return pathlen, rd_posns, rn

            for ncode, nrd_posns, nrn in neighbours(rd_posns, rn):
                npathlen = pathlen + 1
                if (ncode, nrd_posns, nrn) not in visited:
                    visited.add((ncode, nrd_posns, nrn))
                    queue.append((ncode, npathlen, nrd_posns, nrn))
    else:
        pathlen, rd_posns, rn = bfs(code[0], rd_posns, rn)
        pathlen_2, rd_posns_2, rn_2 = bfs(code[1:], rd_posns, rn)
        return pathlen + pathlen_2, rd_posns_2, rn_2


def compute(s: str, nrobots: int) -> int:
    codes = s.strip().splitlines()

    rd_posns_start = tuple(0 + 2j for _ in range(nrobots))
    rn_start = 3 + 2j

    complexity = 0

    pathlen = bfs("0", rd_posns_start, rn_start)

    for code in codes:
        pathlen, *_ = bfs(code, rd_posns_start, rn_start)

        complexity += pathlen * int(code[:-1])

    return complexity


INPUT_S = """\
029A
980A
179A
456A
379A
"""
EXPECTED = 126384


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, EXPECTED),),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s, 2) == expected


INPUT_TXT = Path(__file__).parent / "input.txt"


def main() -> int:
    print(compute(INPUT_S, 2))

    print(compute(INPUT_S, 25))

    with open(INPUT_TXT) as f, support.timing():
        print(compute(f.read(), 25))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
