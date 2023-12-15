import dataclasses
from collections import defaultdict

from aoc2023.utils import Handler


def decode(value: str, split: bool = False) -> int:
    if split:
        char = "-" if "-" in value else "="
        value = value.split(char)[0]
    current_value = 0
    for char in value:
        current_value = (current_value + ord(char)) * 17 % 256
    return current_value


@dataclasses.dataclass
class Box:
    lenses: dict[str, int] = dataclasses.field(init=False, default_factory=dict)

    def operation(self, lens: str) -> None:
        if "-" in lens:
            return self.remove(lens)
        return self.add(lens)

    def remove(self, lens: str) -> None:
        label, _ = lens.split("-")
        if label in self.lenses:
            del self.lenses[label]

    def add(self, lens: str) -> None:
        label, force = lens.split("=")
        self.lenses[label] = int(force)

    def power(self, index: int) -> int:
        return sum((index + 1) * (i + 1) * x for i, x in enumerate(self.lenses.values()))


def part_1(input: list[str]) -> int:
    total = 0
    for hash in input[0].split(","):
        total += decode(hash)
    return total


def part_2(input: list[str]) -> int:
    boxes: dict[int, Box] = defaultdict(Box)
    for lens in input[0].split(","):
        boxes[decode(lens, split=True)].operation(lens)
    return sum(b.power(k) for k, b in boxes.items())


def create_handler(input: list[str]) -> Handler:
    return Handler(
        input=input,
        part_1=part_1,
        part_2=part_2,
    )
