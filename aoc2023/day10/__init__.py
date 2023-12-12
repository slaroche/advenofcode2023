import dataclasses
import enum
import typing as t
from collections import defaultdict

from aoc2023.utils import Handler


class Tile(enum.Enum):
    NW = "J"

    H = "-"
    NE = "L"

    SE = "F"

    V = "|"
    SW = "7"

    S = "S"
    G = "."


H_TILE = [
    Tile.H,
    Tile.S,
    Tile.NE,
    Tile.NW,
    Tile.SE,
    Tile.SW,
]

V_TILE = [
    Tile.V,
    Tile.S,
    Tile.NE,
    Tile.NW,
    Tile.SE,
    Tile.SW,
]


@dataclasses.dataclass
class Pipe:
    value: Tile
    pos: tuple[int, int]
    max_i: int = dataclasses.field(repr=False)
    max_j: int = dataclasses.field(repr=False)
    grid: dict[tuple[int, int], "Pipe"] = dataclasses.field(repr=False)
    is_loop: bool = False
    _is_inside: bool | None = None

    def __post_init__(self) -> None:
        self.is_loop = self.value is Tile.S

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

    @property
    def n_pipe_count(self) -> int:
        count = 0
        if self.i == 0:
            return count
        for i in range(self.i):
            pipe: Pipe = self.grid[(i, self.j)]
            if pipe.is_loop and (
                pipe.value is Tile.H or pipe.value is Tile.NE or pipe.value is Tile.SE
            ):
                count += 1
        return count

    @property
    def w_pipe_count(self) -> int:
        count = 0
        if self.j == 0:
            return count
        for j in range(self.j):
            pipe: Pipe = self.grid[(self.i, j)]
            if pipe.is_loop and (
                pipe.value is Tile.V
                or pipe.value is Tile.S
                or pipe.value is Tile.SW
                or pipe.value is Tile.SE
            ):
                count += 1
        return count

    @property
    def is_inside(self) -> bool:
        if self._is_inside is not None:
            return self._is_inside

        self.is_inside = False
        if not self.is_loop:
            return self.is_inside

        if self.n_pipe_count > 0 and self.w_pipe_count > 0:
            return self.is_inside

        self.is_inside = self.n_pipe_count % 2 != 0 and self.w_pipe_count % 2 != 0
        return self.is_inside


@dataclasses.dataclass
class Cursor:
    current: Pipe
    previous: Pipe

    def __post_init__(self) -> None:
        self.current.is_loop = True

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


def get_start(input: list[str]) -> Pipe:
    grid: dict[tuple[int, int], Pipe] = {}
    start: Pipe = None
    for i, line in enumerate(input):
        for j, tile in enumerate(line):
            pipe = Pipe(Tile(tile), (i, j), len(input) - 1, len(line) - 1, grid)
            grid[(i, j)] = pipe
            if pipe.is_start:
                start = pipe

    if not start:
        raise ValueError()
    return start


def print_grid(grid: dict[tuple[int, int], Pipe]) -> None:
    lines: dict[int, str] = defaultdict(lambda: "")
    for p in grid.values():
        lines[p.i] += p.value.value if p.is_loop else ("*" if p.is_inside else "#")
    for l in lines.values():
        print(l)


def part_1(input: list[str]) -> int:
    start = get_start(input)
    right, left = Cursor.from_start(start)

    total = 1
    while right != left:
        total += 1
        right = Cursor.from_cursor(right)
        left = Cursor.from_cursor(left)
    return total


def part_2(input: list[str]) -> int:
    start = get_start(input)
    right, left = Cursor.from_start(start)
    while right != left:
        right = Cursor.from_cursor(right)
        left = Cursor.from_cursor(left)

    return len([p for p in start.grid.values() if p.is_inside])


def create_handler(input: list[str]) -> Handler:
    return Handler(
        input=input,
        part_1=part_1,
        part_2=part_2,
    )
