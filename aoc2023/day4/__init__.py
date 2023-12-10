import dataclasses
import typing as t
from collections import defaultdict

from aoc2023.utils import Handler


@dataclasses.dataclass
class Card:
    id: int
    numbers: list[int]
    winning_numbers: list[int]

    @classmethod
    def parse(cls, line: str) -> t.Self:
        card, numbers = line.split(":")
        _, id = card.split(" ", maxsplit=1)
        cnumbers, wnumbers = numbers.split("|")
        return cls(
            id=int(id),
            numbers=[int(n) for n in cnumbers.split(" ") if n != ""],
            winning_numbers=[int(n) for n in wnumbers.split(" ") if n != ""],
        )

    @property
    def mathing_numbers(self) -> list[int]:
        return [n for n in self.numbers if n in self.winning_numbers]

    @property
    def mathing_count(self) -> int:
        return len(self.mathing_numbers)

    def total(self) -> int:
        num = self.mathing_numbers.copy()
        total = 0
        if num:
            num.pop()
            total = 1
        for _ in num:
            total = total * 2
        return total


def part_1(input: list[str]) -> int:
    cards = [Card.parse(line) for line in input]
    return sum(c.total() for c in cards)


def part_2(input: list[str]) -> int:
    cards: dict[int, int] = defaultdict(lambda: 1)
    for line in input:
        card = Card.parse(line)
        start = card.id + 1
        end = start + card.mathing_count
        for i in range(start, end):
            cards[i] += cards[card.id]
    return sum(cards.values())


def create_handler(input: list[str]) -> Handler:
    return Handler(
        input=input,
        part_1=part_1,
        part_2=part_2,
    )
