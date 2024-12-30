from pathlib import Path

import pytest

import support


def next_number(n: int) -> int:
    n1 = n * 64
    n ^= n1
    n %= 16777216
    n2 = n // 32
    n ^= n2
    n %= 16777216
    n3 = n * 2048
    n ^= n3
    n = n % 16777216
    return n


def compute(s: str, N: int = 2000) -> int:
    numbers = [int(line) for line in s.splitlines()]

    prices = []
    price_changes = []
    seq_price_maps = []
    for n in numbers:
        secret_numbers = [n]
        monkey_prices = [n % 10]
        monkey_price_changes = []
        for _ in range(N):
            n = next_number(n)
            secret_numbers.append(n)
            monkey_prices.append(n % 10)
            monkey_price_changes.append(monkey_prices[-1] - monkey_prices[-2])
        prices.append(monkey_prices)
        price_changes.append(monkey_price_changes)

        seq_price_map = {}
        for i in range(len(monkey_price_changes) - 3):
            seq = tuple(monkey_price_changes[i: i + 4])
            if seq not in seq_price_map:
                seq_price_map[seq] = monkey_prices[i + 4]

        seq_price_maps.append(seq_price_map)

    sequence_total_prices = {}
    max_price = 0
    seq_max = None
    for seq_price_map in seq_price_maps:
        for seq in seq_price_map:
            if seq in sequence_total_prices:
                continue
            sequence_total_prices[seq] = sum(s.get(seq, 0) for s in seq_price_maps)
            if sequence_total_prices[seq] > max_price:
                max_price = sequence_total_prices[seq]
                seq_max = seq

    return max_price


INPUT_SS = """\
123
"""

INPUT_S = """\
1
2
3
2024
"""
EXPECTED = 23


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, EXPECTED),),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


INPUT_TXT = Path(__file__).parent / "input.txt"


def main() -> int:
    # print(compute(INPUT_SS, 10))

    print(compute(INPUT_S))

    with open(INPUT_TXT) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
