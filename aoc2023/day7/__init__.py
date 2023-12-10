import dataclasses
import pprint
import typing as t
from collections import defaultdict

from aoc2023.utils import Handler

card_values = {
    "2": 1,
    "3": 2,
    "4": 3,
    "5": 4,
    "6": 5,
    "7": 6,
    "8": 7,
    "9": 9,
    "T": 10,
    "J": 0,
    "Q": 12,
    "K": 13,
    "A": 14,
}


def process(ori: dict[str, int], raw: str) -> dict[str, int]:
    if "J" not in ori.keys():
        return dict(ori)

    if ori == {"J": 5}:
        return dict(ori)

    new = {}
    process = False
    for k, v in ori.items():
        if k == "J":
            continue

        elif 1 < v < 5 and not process:
            new[k] = ori[k] + ori["J"]
            process = True
            # print(k, new[k], ori[k], "+" ,ori["J"])

        else:
            new[k] = ori[k]

    if sum(new.values()) != 5:
        new[list(new)[0]] += ori["J"]

    # if raw == "J3737":
    #     breakpoint()
    return new


@dataclasses.dataclass
class Hand:
    raw: str
    cards: dict[str, int]
    bid: int

    @classmethod
    def parse(cls, line: str, part_2: bool = False) -> t.Self:
        raw, bid = line.split(" ")
        cards: dict[str, int] = defaultdict(lambda: 0)
        for c in raw:
            cards[c] += 1
        return cls(
            bid=int(bid),
            cards=dict(cards) if not part_2 else process(cards, raw),
            raw=raw,
        )

    def strength(self) -> int:
        values = self.cards.values()
        v = 0
        if 5 in values:
            v += 500
        if 4 in values:
            v += 400
        if 3 in values:
            v += 300
        if 2 in values:
            v += 50 * len([n for n in values if n == 2])
        return v

    def __gt__(self, hand: t.Self) -> bool:
        if self.strength() != hand.strength():
            return self.strength() > hand.strength()
        for i, _ in enumerate(self.raw):
            if self.raw[i] == hand.raw[i]:
                continue
            return card_values[self.raw[i]] > card_values[hand.raw[i]]
        return False

    def total(self, index: int) -> int:
        rank = index + 1
        return rank * self.bid


def part_1(input: list[str]) -> int:
    # pprint.pprint(sorted(Hand.parse(line) for line in input))
    return sum(
        h.total(i) for i, h in enumerate(sorted(Hand.parse(line) for line in input))
    )


def part_2(input: list[str]) -> int:
    pprint.pprint(sorted(Hand.parse(line, True) for line in input))
    m = sorted(Hand.parse(line, True) for line in input)
    for x in m:
        if sum(x.cards.values()) != 5:
            breakpoint()
    return sum(
        h.total(i) for i, h in enumerate(sorted(Hand.parse(line, True) for line in input))
    )


def create_handler(input: list[str]) -> Handler:
    return Handler(
        input=input,
        part_1=part_1,
        part_2=part_2,
    )
