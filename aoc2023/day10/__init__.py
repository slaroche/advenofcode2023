import dataclasses
import enum

from aoc2023.utils import Handler
import typing as t


class Tile(enum.Enum):
    V = "|"
    H = "-"
    NE = "L"
    NW = "J"
    SE = "F"
    SW = "7"
    S = "S"
    G = "."

connections = {
    Tile.V: [
        Tile.SW,
        Tile.SE,
        Tile.NW,
        Tile.NE,
    ],
    Tile.H: [
        Tile.SW,
        Tile.SE,
        Tile.NW,
        Tile.NE,
    ],
    Tile.NE: [
        Tile.H,
        Tile.V,
        Tile.SW,
        Tile.SE,
        Tile.NW,
    ],
    Tile.NW: [
        Tile.H,
        Tile.V,
        Tile.SW,
        Tile.SE,
        Tile.NE,
    ],
    Tile.SE: [
        Tile.H,
        Tile.V,
        Tile.NW,
        Tile.NE,
        Tile.SW,
    ],
    Tile.SW: [
        Tile.H,
        Tile.V,
        Tile.NW,
        Tile.NE,
        Tile.SE,
    ],
    Tile.S: [
        Tile.H,
        Tile.V,
        Tile.NW,
        Tile.NE,
        Tile.SE,
        Tile.SW,
    ],
}

@dataclasses.dataclass
class Grid:
    height: int
    width: int


@dataclasses.dataclass
class Pipe:
    value: Tile
    pos: tuple[int, int]
    max_i: int = dataclasses.field(repr=False)
    max_j: int= dataclasses.field(repr=False)
    grid: dict[tuple[int, int], "Pipe"] = dataclasses.field(repr=False)

    @property
    def i(self) -> int:
        return self.pos[0]

    @property
    def j(self) -> int:
        return self.pos[1]

    @property
    def n_conn(self) -> t.Optional["Pipe"]:
        if self.i == 0:
            return None
        if not (
            self.value is Tile.V
            or self.value is Tile.S
            or self.value is Tile.NE
            or self.value is Tile.NW
        ):
            return None
        pipe = self.grid[(self.i - 1, self.j)]
        if not (
            pipe.value is Tile.V
            or pipe.value is Tile.S
            or pipe.value is Tile.SW
            or pipe.value is Tile.SE
        ):
            return None
        return pipe


    @property
    def s_conn(self) -> t.Optional["Pipe"]:
        if self.i == self.max_i:
            return None
        if not (
            self.value is Tile.V
            or self.value is Tile.S
            or self.value is Tile.SW
            or self.value is Tile.SE
        ):
            return None
        pipe = self.grid[(self.i + 1, self.j)]
        if not (
            pipe.value is Tile.V
            or pipe.value is Tile.S
            or pipe.value is Tile.NE
            or pipe.value is Tile.NW
        ):
            return None
        return pipe

    @property
    def e_conn(self) -> t.Optional["Pipe"]:
        if self.j == self.max_j:
            return None
        if not (
            self.value is Tile.H
            or self.value is Tile.S
            or self.value is Tile.NE
            or self.value is Tile.SE
        ):
            return None
        pipe = self.grid[(self.i, self.j + 1)]
        if not (
            pipe.value is Tile.H
            or pipe.value is Tile.S
            or pipe.value is Tile.NW
            or pipe.value is Tile.SW
        ):
            return None
        return pipe

    @property
    def w_conn(self) -> t.Optional["Pipe"]:
        if self.j == 0:
            return None
        if not (
            self.value is Tile.H
            or self.value is Tile.S
            or self.value is Tile.NW
            or self.value is Tile.SW
        ):
            return None
        pipe = self.grid[(self.i, self.j -1)]
        if not (
            pipe.value is Tile.H
            or pipe.value is Tile.S
            or pipe.value is Tile.NE
            or pipe.value is Tile.SE
        ):
            return None
        return pipe

    @property
    def all_conn(self) -> list["Pipe"]:
        return [c for c in [
            self.n_conn,
            self.s_conn,
            self.e_conn,
            self.w_conn,
        ] if c]

    @property
    def left(self) -> "Pipe":
        if len(self.all_conn) != 2:
            raise ValueError()
        return self.all_conn[0]

    @property
    def right(self) -> "Pipe":
        if len(self.all_conn) != 2:
            raise ValueError()
        return self.all_conn[1]

    def next(self, after: "Pipe") -> tuple["Pipe", "Pipe"]:
        if self.right != after:
            return self.right, self
        return self.left, self


    @property
    def is_connected(self) -> bool:
        return self.value is Tile.S or self.all_conn
    
    @property
    def is_start(self) -> bool:
        return self.value is Tile.S



def part_1(input: list[str]) -> int:
    total = 1
    grid: dict[tuple[int, int], Pipe] = {}
    start: Pipe = None
    for i, line in enumerate(input):
        for j, tile in enumerate(line):
            pipe = Pipe(
                Tile(tile), 
                (i, j), 
                len(input) - 1,
                len(line) - 1,
                grid
            )
            grid[(i, j)] = pipe
            if pipe.is_start:
                start = pipe

    if not start:
        return total

    right: Pipe = start.right
    previous_right: Pipe = start

    left: Pipe = start.left
    previous_left: Pipe = start

    print("start", start)
    print("right", start.right, "left", start.left)
    while right != left:
        total += 1
        right, previous_right = right.next(previous_right)
        left, previous_left = left.next(previous_left)
        print(total, "right", right, "left", left, "is different", right != left)
    return total


def part_2(input: list[str]) -> int:
    total = 0

    return total


def create_handler(input: list[str]) -> Handler:
    return Handler(
        input=input,
        part_1=part_1,
        part_2=part_2,
    )
