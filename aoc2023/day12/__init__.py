import dataclasses
import itertools
import re
import typing as t
from collections import defaultdict

from aoc2023.utils import Handler


def create_permutation(loop: int, arr: list[str] | None = None) -> list[str]:
    if loop == 1:
        return arr or [".", "#"]
    return create_permutation(
        arr=[
            l + r
            for l, r in itertools.product(
                arr or [".", "#"],
                [".", "#"],
            )
        ],
        loop=loop - 1,
    )


@dataclasses.dataclass
class Row:
    record: str
    groups: list[int]
    multiplier: dataclasses.InitVar[int] = 1
    re: t.Pattern = dataclasses.field(init=False)

    def __post_init__(self, multiplier: int = 1) -> None:
        self.re = re.compile(
            r"^[.]*"
            + r"[.]+".join(["#{" + str(x) + "}" for x in self.groups])
            + r"[.]*$",
        )
        for _ in range(multiplier - 1):
            self.groups.extend(self.groups)
            self.record += self.record

    @classmethod
    def parse(cls, line: str, multiplier: int = 1) -> t.Self:
        record, groups = line.split(" ")
        return cls(
            record=record,
            groups=[int(x) for x in groups.split(",")],
            multiplier=multiplier,
        )

    def is_valid_arr(self, arr: str) -> bool:
        return bool(self.re.match(arr))

    def generate_arr(self) -> t.Iterator[str]:
        for p in create_permutation(self.record.count("?")):
            mapping = defaultdict(lambda: None)
            for x, i in zip(p, self.get_unknown_pos()):
                mapping[i] = x
            arr = "".join(
                s if (s := mapping[i]) else x for i, x in enumerate(self.record)
            )
            if arr.count("#") == sum(self.groups):
                yield arr

    def get_unknown_pos(self) -> list[int]:
        return [i for i, x in enumerate(self.record) if x == "?"]


def part_1(input: list[str]) -> int:
    count = []
    for line in input:
        row: Row = Row.parse(line)
        for arr in row.generate_arr():
            count.append(row.is_valid_arr(arr))

    return sum(x for x in count if x)


def part_2(input: list[str]) -> int:
    count = []
    for line in input:
        row = Row.parse(line, 5)
        for arr in row.generate_arr():
            count.append(row.is_valid_arr(arr))

    return sum(x for x in count if x)


def create_handler(input: list[str]) -> Handler:
    return Handler(
        input=input,
        part_1=part_1,
        part_2=part_2,
    )
