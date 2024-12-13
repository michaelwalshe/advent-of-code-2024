import heapq
import re
from pathlib import Path
from typing import NamedTuple

import pytest

import support


class point(NamedTuple):
    x: int
    y: int


def compute(s: str) -> int:
    machines = []
    for m in s.split("\n\n"):
        buttons = {}
        for line in m.splitlines():
            if line.startswith("Prize:"):
                prize_x, prize_y = re.findall(r"X=(\d+), Y=(\d+)", line)[0]
            elif line.startswith("Button "):
                button, x, y = re.findall(r"Button (A|B): X\+(\d+), Y\+(\d+)", line)[0]
                buttons[button] = point(int(x), int(y))
        machines.append(
            (
                buttons,
                point(int(prize_x) + 10000000000000, int(prize_y) + 10000000000000),
            )
        )

    costs = []
    for buttons, prize in machines:
        # b = (Y - (Ay/Ax)X) * (Ax / (AxBy - AyBx))
        b = (prize.y - (buttons["A"].y / buttons["A"].x) * prize.x) * (
            buttons["A"].x
            / (buttons["A"].x * buttons["B"].y - buttons["A"].y * buttons["B"].x)
        )
        # a = (X - Bx) / Ax
        a = (prize.x - buttons["B"].x * b) / buttons["A"].x

        def check_button(n: float) -> bool:
            return abs(n - round(n)) < 0.001

        if check_button(a) and check_button(b):
            costs.append(3 * round(a) + round(b))

    return sum(costs)


INPUT_S = """\
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""
EXPECTED = 875318608908


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
