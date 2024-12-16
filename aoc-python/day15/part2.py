from pathlib import Path
from typing import NamedTuple

import pytest

import support


class Point(NamedTuple):
    x: int
    y: int


class Box(NamedTuple):
    l: Point
    r: Point


def print_warehouse(walls: set[Point], boxes: list[Box], robot: Point) -> None:
    max_x = max(p.x for p in walls)
    max_y = max(p.y for p in walls)

    print("Warehouse:")
    x = y = 0
    while True:
        if Point(x, y) in walls:
            print("#", end="")
            x += 1
        elif Box(Point(x, y), Point(x + 1, y)) in boxes:
            print("[]", end="")
            x += 2
        elif Point(x, y) == robot:
            print("@", end="")
            x += 1
        else:
            print(".", end="")
            x += 1
        if x > max_x:
            print("")
            x = 0
            y += 1
        if y > max_y:
            break


def unpack_boxes(boxes: list[Box]) -> list[Point]:
    return [p for b in boxes for p in b]


def move_box(box: Box, move: Point) -> Box:
    return Box(
        Point(box.l.x + move.x, box.l.y + move.y),
        Point(box.r.x + move.x, box.r.y + move.y),
    )


MOVE_MAP = {
    "<": Point(-1, 0),
    ">": Point(1, 0),
    "^": Point(0, -1),
    "v": Point(0, 1),
}


def compute(s: str) -> int:
    warehouse_s, moves_s = s.split("\n\n")
    walls = set()
    boxes = []
    i = j = 0
    for row in warehouse_s.splitlines():
        for cell in row:
            if cell == "#":
                walls.update((Point(i, j), Point(i + 1, j)))
            elif cell == "O":
                boxes.append(Box(Point(i, j), Point(i + 1, j)))
            elif cell == "@":
                robot = Point(i, j)
            i += 2
        i = 0
        j += 1
    moves = [MOVE_MAP[c] for c in moves_s if c in "<>^v"]

    for move in moves:
        # print_warehouse(walls, boxes, robot)
        next_obj = Point(robot.x + move.x, robot.y + move.y)
        if next_obj in walls:
            continue
        if next_obj in unpack_boxes(boxes):
            # Get boxes that are directly in front of the robot
            boxes_to_move = [b for b in boxes if b.l == next_obj or b.r == next_obj]
            # Initialise list of boxes that have been nudged by the robot (directly
            # or indirectly)
            moved_boxes = boxes_to_move.copy()
            while True:
                # Get a box that had been moved, move it in same direction
                latest_box = moved_boxes.pop()
                latest_box_moved = move_box(latest_box, move)
                # If there's a wall, this move is impossible
                if latest_box_moved.l in walls or latest_box_moved.r in walls:
                    to_move = False
                    break
                # All boxes excluding the one currently being checked
                boxes_no_latest = [b for b in boxes if b != latest_box]

                if any(
                    latest_box_moved.l == p or latest_box_moved.r == p
                    for p in unpack_boxes(boxes_no_latest)
                ):
                    # If the box that was just moved nudges another box(es),
                    # find out which they are and add them to the list to check
                    next_boxes = [
                        b
                        for b in boxes_no_latest
                        if any(
                            b.l == p or b.r == p
                            for p in unpack_boxes([latest_box_moved])
                        )
                    ]
                    boxes_to_move.extend(next_boxes)
                    moved_boxes.extend(next_boxes)
                    continue
                # If the box that was just moved doesn't nudge any other boxes
                to_move = True
                if not moved_boxes:
                    break
            if to_move:
                # Double checking that we don't move a box twice,
                # even though that shouldnt happen
                for box in set(boxes_to_move):
                    boxes.remove(box)
                    boxes.append(move_box(box, move))
                robot = next_obj
                continue
        else:
            robot = next_obj

    print_warehouse(walls, boxes, robot)
    return sum(100 * b.l.y + b.l.x for b in boxes)


INPUT_V_S = """\
#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^
"""

INPUT_S = """\
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
"""
EXPECTED = 9021


@pytest.mark.parametrize(
    ("input_s", "expected"),
    ((INPUT_S, EXPECTED),),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


INPUT_TXT = Path(__file__).parent / "input.txt"


def main() -> int:
    print(compute(INPUT_V_S))
    print(compute(INPUT_S))

    with open(INPUT_TXT) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
