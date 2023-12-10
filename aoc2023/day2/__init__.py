import collections
import dataclasses
import typing as t

from aoc2023.utils import Handler
from aoc2023.utils import multiply

config = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


@dataclasses.dataclass
class Dice:
    count: int
    color: str


Set: t.TypeAlias = dict[str, int]


def is_set_possible(game_set: Set) -> bool:
    for color, count in game_set.items():
        if config[color] < count:
            return False
    return True


@dataclasses.dataclass
class Power:
    red: int | None = None
    green: int | None = None
    blue: int | None = None

    def set(self, color: str, counts: list[int]) -> None:
        setattr(self, color, max(counts))

    @property
    def total(self) -> int:
        return multiply(x for x in [self.red, self.blue, self.green] if x)


@dataclasses.dataclass
class Game:
    id: int
    dices: list[Set] = dataclasses.field(default_factory=list)

    def is_possible(self) -> bool:
        return all(is_set_possible(s) for s in self.dices)

    @property
    def power(self) -> Power:
        counts_by_color = collections.defaultdict(list)
        for s in self.dices:
            for color, count in s.items():
                counts_by_color[color].append(count)
        power = Power()
        for color, counts in counts_by_color.items():
            power.set(color, counts)
        return power


def format_line(line: str) -> Game:
    game_str, line = line.split(": ")
    game: Game = Game(int(game_str.split(" ")[1]))
    for set_str in line.split("; "):
        game.dices.append(
            {
                dice_str.split(" ")[1].replace("\n", ""): int(dice_str.split(" ")[0])
                for dice_str in set_str.split(", ")
            }
        )
    return game


def part_1(input: list[str]) -> int:
    total: int = 0
    for line in input:
        game = format_line(line)
        if not game.is_possible():
            continue
        total += game.id
    return total


def part_2(input: list[str]) -> int:
    total: int = 0
    for line in input:
        game = format_line(line)
        total += game.power.total
    return total


def create_handler(input: list[str]) -> Handler:
    return Handler(
        input=input,
        part_1=part_1,
        part_2=part_2,
    )
