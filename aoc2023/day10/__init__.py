import dataclasses
import enum
import typing as t

from aoc2023.utils import Handler


class Tile(enum.Enum):
    V = "|"
    H = "-"
    NE = "L"
    NW = "J"
    SE = "F"
    SW = "7"
    S = "S"
    G = "."


@dataclasses.dataclass
class Pipe:
    value: Tile
    pos: tuple[int, int]
    max_i: int = dataclasses.field(repr=False)
    max_j: int = dataclasses.field(repr=False)
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
        pipe = self.grid[(self.i, self.j - 1)]
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
        return [
            c
            for c in [
                self.n_conn,
                self.s_conn,
                self.e_conn,
                self.w_conn,
            ]
            if c
        ]

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
    def is_start(self) -> bool:
        return self.value is Tile.S


@dataclasses.dataclass
class Cursor:
    current: Pipe
    previous: Pipe

    @classmethod
    def from_start(cls, start: Pipe) -> tuple[t.Self, t.Self]:
        right = cls(start.right, start)
        left = cls(start.left, start)
        return right, left

    @classmethod
    def from_cursor(cls, cursor: t.Self) -> t.Self:
        return cls(*cursor.current.next(cursor.previous))

    def __eq__(self, __value: t.Self) -> bool:
        return self.current == __value.current


def part_1(input: list[str]) -> int:
    grid: dict[tuple[int, int], Pipe] = {}
    start: Pipe = None
    for i, line in enumerate(input):
        for j, tile in enumerate(line):
            pipe = Pipe(Tile(tile), (i, j), len(input) - 1, len(line) - 1, grid)
            grid[(i, j)] = pipe
            if pipe.is_start:
                start = pipe

    if not start:
        return total

    right, left = Cursor.from_start(start)

    total = 1
    while right != left:
        total += 1
        right = Cursor.from_cursor(right)
        left = Cursor.from_cursor(left)
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
