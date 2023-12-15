import typing as t
from collections import defaultdict
from pprint import pprint

from aoc2023.utils import Handler


def rotated(lines: t.Iterable[str]) -> t.Iterator[str]:
    yield from map("".join, zip(*lines))


def tilt(lines: t.Iterable[str]) -> t.Iterator[str]:
    yield from [
        "#".join("O" * sub.count("O") + "." * sub.count(".") for sub in line.split("#"))
        for line in lines
    ]


def part_1(input: list[str]) -> int:
    total = 0
    for i, line in enumerate(rotated(tilt(rotated(input)))):
        print(line)
        total += line.count("O") * (len(input) - i)
    return total


def cycle(input: t.Iterable[str]) -> t.Iterator[str]:
    # north
    input = rotated(tilt(rotated(input)))
    # west
    input = tilt(input)
    # south
    input = reversed(rotated(tilt(rotated(reversed(input)))))
    # east
    yield from rotated(reversed(rotated(tilt(rotated(reversed(rotated(input)))))))


def part_2(input: list[str]) -> int:
    d = defaultdict(lambda: (0, 0))

    for j in range(1000):
        input = cycle(input)
        total = 0
        for i, line in enumerate(input):
            total += line.count("O") * (len(input) - i)
        d[total] = (d[total][0] + 1, j)
        pprint({k: v for k, v in d.items() if v[0] > 2})

    return total


def create_handler(input: list[str]) -> Handler:
    return Handler(
        input=input,
        part_1=part_1,
        part_2=part_2,
    )
