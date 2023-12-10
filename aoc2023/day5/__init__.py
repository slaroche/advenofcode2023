import dataclasses
import typing as t

from aoc2023.utils import Handler


def parse_seeds(line: str) -> list[int]:
    _, numbers = line.split(":", 1)
    return [int(n) for n in numbers.split(" ") if n != ""]


def part_1(input: list[str]) -> int:
    src: list[int] = []
    dest: list[int] = []
    map: dict[tuple[int, int], int] = {}

    for i, line in enumerate(input):
        if i == 0:
            dest = parse_seeds(line)
            continue

        if i == 1:
            continue

        if line == "" or line == "end":
            src = dest.copy()
            dest = []
            for s in src:
                d = None
                for b, dmap in map.items():
                    l, u = b
                    if l <= s < u:
                        d = dmap + (s - l)
                dest.append(d or s)
            continue

        if line[0].isalpha():
            map = {}
            continue

        d, s_str, r = line.split(" ")
        s = int(s_str)
        d = int(d)
        r = int(r)
        map[(s, s + r)] = d

    return min(dest)


@dataclasses.dataclass
class Datum:
    value: int
    range: int

    @property
    def upper_bound(self) -> int:
        return self.value + self.range


@dataclasses.dataclass
class Mapping:
    src: int
    dest: int

    range: int

    @property
    def src_upper_bound(self) -> int:
        return self.src + self.range

    @property
    def dest_upper_bound(self) -> int:
        return self.dest + self.range

    @classmethod
    def parse(cls, line: str) -> t.Self:
        d, s, r = line.split(" ")
        return cls(
            src=int(s),
            dest=int(d),
            range=int(r),
        )

    def get_seg(self, datum: Datum) -> tuple[list[Datum], list[Datum]]:
        seg = []
        diff = self.dest - self.src
        l = max(self.src, datum.value)
        u = min(self.src_upper_bound, datum.upper_bound)
        if l > u:
            return [], [datum]
        if datum.value < l:
            seg.append(dataclasses.replace(datum, range=l - datum.value))
        if datum.upper_bound > u:
            seg.append(
                Datum(
                    value=datum.upper_bound + 1,
                    range=datum.upper_bound - u,
                )
            )
        return [Datum(value=l + diff, range=u - l)], seg


def parse_data(line: str) -> list[Datum]:
    _, numbers = line.split(":", 1)
    data = []
    value = 0
    for i, range_ in enumerate(int(n) for n in numbers.split(" ") if n != ""):
        if i % 2:
            data.append(Datum(value, range_))
        else:
            value = range_
    return data


def part_2(input: list[str]) -> int:
    data: list[Datum] = []
    dest: list[Datum] = []

    for i, line in enumerate(input):
        if i == 0:
            dest = parse_data(line)
            continue

        if line == "":
            continue

        if line[0].isalpha():
            data.extend(dest.copy())
            dest = []
            continue

        mapping = Mapping.parse(line)

        src = []
        for datum in data:
            converted_datum, seg = mapping.get_seg(datum)
            dest.extend(converted_datum)
            src.extend(seg)
        data = src.copy()

    return min(d.value for d in data)


def create_handler(input: list[str]) -> Handler:
    return Handler(
        input=input,
        part_1=part_1,
        part_2=part_2,
    )
