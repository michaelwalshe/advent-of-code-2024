from collections import defaultdict
from pathlib import Path

def part2(data):
    prices = []
    for secret in map(int, data):
        price = []
        for _ in range(2000):
            secret = ((secret * 64) ^ secret) % 16777216
            secret = ((secret // 32) ^ secret) % 16777216
            secret = ((secret * 2048) ^ secret) % 16777216
            price.append(secret % 10)
        prices.append(price)

    changes = [[b - a for a, b in zip(p, p[1:])] for p in prices]

    """
    caches = []
    seq_keys = set()

    for buyer_idx, change in enumerate(changes):
        cache = {}
        for i in range(len(change) - 3):
            key = tuple(change[i : i + 4])
            if key in cache:
                continue
            cache[key] = prices[buyer_idx][i + 4]
            seq_keys.add(key)
        caches.append(cache)

    amounts = [sum(cache.get(key, 0) for cache in caches) for key in seq_keys]
    max_amount = max(amounts)
    """

    amounts = defaultdict(int)
    for buyer_idx, change in enumerate(changes):
        keys = set()
        for i in range(len(change) - 3):
            key = tuple(change[i : i + 4])
            if key in keys:
                continue
            amounts[key] += prices[buyer_idx][i + 4]
            keys.add(key)
    max_amount = max(amounts.values())

    return max_amount


INPUT_TXT = Path(__file__).parent / "input.txt"

INPUT_S = """\
1
10
100
2024
"""
EXPECTED = 23

print(part2(INPUT_S.splitlines()))