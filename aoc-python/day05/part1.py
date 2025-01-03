from pathlib import Path
from itertools import combinations
from collections import defaultdict
import pytest

import support


def check_update(update: list[str], rules: dict[str, str]) -> bool:
    seen = {update[0]}
    for i in range(1, len(update)):
        if update[i] in rules and not rules[update[i]].isdisjoint(seen):
            return False
        seen.add(update[i])
    return True


def compute(s: str) -> int:
    rules_s, updates_s = s.strip().split('\n\n')
    rules = defaultdict(set)
    for rule_s in rules_s.split('\n'):
        key, value = rule_s.split('|')
        rules[key].add(value)

    updates = [p.split(",") for p in updates_s.split('\n')]

    # corrected_updates = []
    # for update in updates:
    #     if check_update(update, rules):
    #         corrected_updates.append(update)
    #         continue
    #     for new_update in combinations(update, len(update)):
    #         if check_update(new_update, rules):
    #             corrected_updates.append(new_update)
    #             break

    tot = 0
    for update in updates:
        print(update)
        if check_update(update, rules):
            print(int(update[len(update) // 2]))
            tot += int(update[len(update) // 2])
    return tot


INPUT_S = '''\
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
'''
EXPECTED = 143


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


INPUT_TXT = Path(__file__).parent / 'input.txt'


def main() -> int:
    print(compute(INPUT_S))

    with open(INPUT_TXT) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
