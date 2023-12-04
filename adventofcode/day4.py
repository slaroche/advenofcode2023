from collections import defaultdict
import dataclasses
import typing as t

from adventofcode.utils import Result


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

    def total(self) -> int:
        num = self.mathing_numbers.copy()
        total = 0
        if num:
            num.pop()
            total = 1
        for _ in num:
            total = total * 2
        return total


def first_puzzle(input: list[str]) -> int:
    cards = [Card.parse(line) for line in input]
    return sum(c.total() for c in cards)


def second_puzzle(input: list[str]) -> int:
    cards: dict[int,int] = defaultdict(lambda: 1)
    for line in input:
        card = Card.parse(line)
        start = card.id + 1
        end = start + len(card.mathing_numbers)
        for i in range(start, end):
            cards[i] += cards[card.id]

    return sum(cards.values())


def run(input: list[str]) -> Result:
    return Result(
        answer_1=first_puzzle(input),
        answer_2=second_puzzle(input),
    )
