from pathlib import Path

import pytest

import support


move_map = {
    "<": (-1, 0),
    ">": (1, 0),
    "^": (0, -1),
    "v": (0, 1),
}


def print_warehouse(walls, boxes, robot):
    max_x = max(x for x, _ in walls)
    max_y = max(y for _, y in walls)

    for j in range(max_y + 1):
        for i in range(max_x + 1):
            if (i, j) in walls:
                print("#", end="")
            elif (i, j) in boxes:
                print("O", end="")
            elif (i, j) == robot:
                print("@", end="")
            else:
                print(".", end="")
        print()


def compute(s: str) -> int:
    warehouse_s, moves_s = s.split("\n\n")
    walls = set()
    boxes = []
    for j, row in enumerate(warehouse_s.splitlines()):
        for i, cell in enumerate(row):
            if cell == "#":
                walls.add((i, j))
            elif cell == "O":
                boxes.append((i, j))
            elif cell == "@":
                robot = (i, j)
    moves = [move_map[c] for c in moves_s if c in "<>^v"]

    for move in moves:
        # print_warehouse(walls, boxes, robot)
        next_obj = (robot[0] + move[0], robot[1] + move[1])
        if next_obj in walls:
            continue
        if next_obj in boxes:
            boxes_to_move = [next_obj]
            new_box = (next_obj[0] + move[0], next_obj[1] + move[1])
            while True:
                if new_box in walls:
                    to_move = False
                    break
                if new_box in boxes:
                    boxes_to_move.append(new_box)
                    new_box = (new_box[0] + move[0], new_box[1] + move[1])
                    continue
                to_move = True
                break
            if to_move:
                for box in boxes_to_move:
                    boxes.remove(box)
                    boxes.append((box[0] + move[0], box[1] + move[1]))
                robot = next_obj
                continue
        else:
            robot = next_obj

    print_warehouse(walls, boxes, robot)
    return sum(100 * y + x for x, y in boxes)


INPUT_V_S = """\
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<
"""
EXPECTED_V_S = 2028

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
EXPECTED = 10092


@pytest.mark.parametrize(
    ("input_s", "expected"),
    (
        (INPUT_S, EXPECTED),
        (INPUT_V_S, EXPECTED_V_S),
    ),
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
