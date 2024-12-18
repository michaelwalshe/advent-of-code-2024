from pathlib import Path
import re

import pytest

import support


def compute(s: str) -> int:
    reg = {}
    regs_s, prog_s = s.split("\n\n")
    for line in regs_s.splitlines():
        r, v = re.findall(r"Register ([A-C]): (\d+)", line)[0]
        reg[r] = int(v)
    program = list(map(int, prog_s.split(":")[1].split(",")))

    def combo(operand: int) -> int:
        assert operand != 7, "Invalid operand"
        combo_operand = operand
        if operand == 4:
            combo_operand = reg["A"]
        elif operand == 5:
            combo_operand = reg["B"]
        elif operand == 6:
            combo_operand = reg["C"]
        return combo_operand

    def compute_output() -> list[int]:
        out = []
        ip = 0
        while ip < len(program) - 1:
            opcode = program[ip]
            operand = program[ip + 1]

            if opcode == 0:
                # adv -- A division
                reg["A"] = reg["A"] // (2 ** combo(operand))
            elif opcode == 1:
                # bxl - bitwise XOR of B
                reg["B"] = reg["B"] ^ operand
            elif opcode == 2:
                # bst -- combo mod 8
                reg["B"] = combo(operand) % 8
            elif opcode == 3:
                # jnx - jump
                if reg["A"] != 0:
                    ip = operand
                    continue
            elif opcode == 4:
                # bxc -- bitwise XOR of B and C
                reg["B"] = reg["B"] ^ reg["C"]
            elif opcode == 5:
                # out
                out.append(combo(operand) % 8)
            elif opcode == 6:
                # bdv -- A division to B
                reg["B"] = reg["A"] // (2 ** combo(operand))
            elif opcode == 7:
                # cdv -- A division to C
                reg["C"] = reg["A"] // (2 ** combo(operand))

            ip += 2

        return out

    # The input program is a loop which outputs once each time. It is
    # entirely dependent on register A, and specifically each 3 bits
    # of A control the corresponding output
    test_a = 0
    for i in range(len(program)):
        check_output = program[len(program) - i - 1:]
        add = 0
        while True:
            test_a2 = (test_a * 8) + add
            reg["A"] = test_a2
            output = compute_output()
            if output == check_output:
                test_a = test_a2
                break
            add += 1

    return test_a


INPUT_S = """\
Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0
"""
EXPECTED = 117440


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
