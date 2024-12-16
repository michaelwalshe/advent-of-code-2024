from itertools import product
import math as m
from pathlib import Path
import re
import pytest

import support


def print_grid(points, max_x, max_y):
    grid = [["." for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    for x, y in points:
        grid[y][x] = "#"
    for row in grid:
        print("".join(row))


def move_robot(x, y, vx, vy, max_x, max_y, seconds):
    for _ in range(seconds):
        x2 = x + vx
        y2 = y + vy
        if x2 < 0:
            x2 = max_x + x2 + 1
        elif x2 > max_x:
            x2 = x2 - max_x - 1
        if y2 < 0:
            y2 = max_y + y2 + 1
        elif y2 > max_y:
            y2 = y2 - max_y - 1
        x = x2
        y = y2
    return x, y


# The robots cycle at just < 11000 seconds, so the tree is somewhere there
def compute(s: str, max_x=10, max_y=7, max_secs=11000) -> int:
    robots = []
    for line in s.splitlines():
        x, y, vx, vy = map(int, re.findall(r"-?\d+", line))
        robots.append((x, y, vx, vy))

    seconds = 0
    while seconds < max_secs:
        new_robots = []
        for x, y, vx, vy in robots:
            new_robots.append((*move_robot(x, y, vx, vy, max_x, max_y, 1), vx, vy))
        robots = new_robots

        robots_set = set((x, y) for x, y, *_ in new_robots)

        # Check if from one robot, we can reach a large number of others
        touched = 0
        for x, y in robots_set:
            stack = [(x, y)]
            visited = set(stack)
            while stack:
                x, y = stack.pop()
                for dx, dy in product((-1, 0, 1), repeat=2):
                    if dx == dy == 0:
                        continue
                    x2 = x + dx
                    y2 = y + dy
                    if (x2, y2) not in visited and (x2, y2) in robots_set:
                        stack.append((x2, y2))
                        visited.add((x2, y2))
            touched = max(touched, len(visited))

        seconds += 1

        if touched > 25:
            # THis may look like a tree, check it...
            print_grid([(x, y) for x, y, *_ in new_robots], max_x, max_y)
            print(seconds)
            if input("Continue? ").lower() != "y":
                break

    return seconds


INPUT_TXT = Path(__file__).parent / "input.txt"


def main() -> int:
    with open(INPUT_TXT) as f, support.timing():
        print(compute(f.read(), 100, 102))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
