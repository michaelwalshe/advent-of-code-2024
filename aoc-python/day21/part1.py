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


def neighbours(
    code: str, rd1: complex, rd2: complex, rn1: complex
) -> list[tuple[str, str, complex, complex, complex]]:
    # Return the next possible states from the current state
    states = set()
    for dir in "A^<v>":
        code_next = code
        rd1_next = rd1
        rd2_next = rd2
        rn1_next = rn1
        # For each next button we can press, check what that would
        # do to the rest of the robots
        # If an A is pressed, that triggers checking the next level of
        # robots
        if dir == "A":
            if DIRECTION_KEYPAD[rd1] == "A":
                if DIRECTION_KEYPAD[rd2] == "A":
                    code_next = code + NUMERIC_KEYPAD[rn1]
                else:
                    rn1_next = move_robot(rn1, DIRECTION_KEYPAD[rd2], "N")
            else:
                rd2_next = move_robot(rd2, DIRECTION_KEYPAD[rd1], "D")
        else:
            rd1_next = move_robot(rd1, dir, "D")

        if code_next != code or rd1_next != rd1 or rd2_next != rd2 or rn1_next != rn1:
            states.add((code_next, dir, rd1_next, rd2_next, rn1_next))

    # This can return invalid combos (i.e. over blanks) so filter
    # those out
    return [s for s in states if all(e is not None for e in s)]


@cache
def bfs(code: str, rd1: complex, rd2: complex, rn1: complex) -> str:
    if len(code) == 1:
        visited = {("", rd1, rd2, rn1)}
        queue = deque([("", "", rd1, rd2, rn1)])

        while queue:
            cur_code, path, rd1, rd2, rn1 = queue.popleft()

            if cur_code == code:
                return path, rd1, rd2, rn1

            for ncode, move, nrd1, nrd2, nrn1 in neighbours(cur_code, rd1, rd2, rn1):
                npath = path + move
                if (ncode, nrd1, nrd2, nrn1) not in visited:
                    visited.add((ncode, nrd1, nrd2, nrn1))
                    queue.append((ncode, npath, nrd1, nrd2, nrn1))
    else:
        path, rd1, rd2, rn1 = bfs(code[0], rd1, rd2, rn1)
        path2, rd1_2, rd2_2, rn1_2 = bfs(code[1:], rd1, rd2, rn1)
        return path + path2, rd1_2, rd2_2, rn1_2


def compute(s: str) -> int:
    codes = s.strip().splitlines()

    rd1_start = 0 + 2j
    rd2_start = 0 + 2j
    rn1_start = 3 + 2j

    complexity = 0

    path = bfs("0", rd1_start, rd2_start, rn1_start)

    for code in codes:
        path, *_ = bfs(code, rd1_start, rd2_start, rn1_start)

        complexity += len(path) * int(code[:-1])

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
    assert compute(input_s) == expected


INPUT_TXT = Path(__file__).parent / "input.txt"


def main() -> int:
    print(compute(INPUT_S))

    with open(INPUT_TXT) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
