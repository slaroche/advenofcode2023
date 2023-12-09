import dataclasses
import typing as t
from collections import defaultdict

from adventofcode.utils import Result


class Pos(t.NamedTuple):
    x: int
    y: int


@dataclasses.dataclass
class ParseResult:
    value: int
    skip: list[Pos]


_skip = []


def should_skip(x: int, y: int) -> bool:
    if (x, y) in _skip:
        return True
    return False


def skip_pos(x: int, y: int) -> None:
    _skip.append((x, y))


def is_symbol(value: str) -> bool:
    if value != "." and not value.isdecimal():
        return True
    return False


def parse_part_number(line: str) -> tuple[int, int]:
    digits = []
    for x in line:
        if x.isdecimal():
            digits.append(x)
        else:
            break
    return int("".join(digits)), len(digits)


def contains_symbol(line: str) -> bool:
    for value in line:
        if is_symbol(value):
            return True
    return False


def get_line(lines: list[str], y: int) -> str | None:
    if y < 0:
        return None
    if len(lines) <= y:
        return None
    try:
        return lines[y]
    except:
        return None


def get_value(line: str, x: int) -> str | None:
    if x < 0:
        return None
    if len(line) <= x:
        return None
    try:
        return line[x]
    except:
        return None


def parse(
    current: str,
    x: int,
    y: int,
    previous: str | None,
    after: str | None,
) -> int | None:
    if not current[x].isdecimal():
        return None

    part, size = parse_part_number(current[x:])
    should_return = False

    # skip following digits
    for _x in range(x + 1, x + size):
        skip_pos(x=_x, y=y)

    # horizontal
    value = get_value(current, x=x - 1)
    if value and is_symbol(value):
        should_return = True

    value = get_value(current, x=x + size)
    if not should_return and value and is_symbol(value):
        should_return = True

    # vertival
    start = x
    if x > 0:
        start -= 1

    until = x + size
    if x + size < len(current) - 1:
        until += 1

    if not should_return and previous and contains_symbol(previous[start:until]):
        should_return = True

    if not should_return and after and contains_symbol(after[start:until]):
        should_return = True

    if should_return:
        return part
    return None


def find_part(line: str, x: int) -> int | None:
    # find first
    if not line[x].isdecimal():
        return None
    start = x
    for value in line[:x][::-1]:
        if not value.isdecimal():
            break
        start -= 1
    part, _ = parse_part_number(line[start:])
    return part


def parse_gear(
    x: int,
    current: str,
    previous: str | None,
    after: str | None,
) -> list[tuple[int, str]]:
    pos = []
    # horizontal
    pos.append((x - 1, current))
    pos.append((x + 1, current))

    # vertical
    # 1.., .1., ..1, 1.1, 11., .11, 111
    #
    if previous:
        pos.append((x - 1, previous))
        pos.append((x, previous))
        pos.append((x + 1, previous))

    if after:
        pos.append((x - 1, after))
        pos.append((x, after))
        pos.append((x + 1, after))

    return pos


def part_1(input: list[str]) -> int:
    parts = []
    for y, line in enumerate(input):
        for x, value in enumerate(line):
            if should_skip(x, y):
                continue
            if value == ".":
                continue

            part = parse(
                current=line,
                x=x,
                y=y,
                previous=get_line(input, y=y - 1),
                after=get_line(input, y=y + 1),
            )
            if part:
                parts.append(part)
    return sum(parts)


def part_2(input: list[str]) -> int:
    gears: list[int] = []
    for y, line in enumerate(input):
        for x, value in enumerate(line):
            if value != "*":
                continue
            pos = parse_gear(
                x,
                current=line,
                previous=get_line(input, y=y - 1),
                after=get_line(input, y=y + 1),
            )
            i_by_l = defaultdict(list)
            for i, l in pos:
                i_by_l[l].append(i)
            parts: list[int] = []
            for l, xs in i_by_l.items():
                p = {x for x in [find_part(l, x_) for x_ in xs] if x is not None}
                parts.extend(p)

            if len(parts) != 2:
                continue
            gears.append(parts[0] * parts[1])

    return sum(gears)


def run(input: list[str]) -> Result:
    return Result(
        input=input,
        part_1=part_1,
        part_2=part_2,
    )
