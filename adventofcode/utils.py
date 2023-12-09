import dataclasses
import enum
import os
import typing as t

PuzzleFn: t.TypeAlias = t.Callable[[list[str]], int]


@dataclasses.dataclass
class Result:
    input: list[str]
    part_1: PuzzleFn
    part_2: PuzzleFn

    def print_answers(self) -> None:
        self.print_part_1()
        self.print_part_2()

    def print_part_1(self) -> None:
        print(f"Part 1 answer: {self.part_1(self.input)}")

    def print_part_2(self) -> None:
        print(f"Part 2 answer: {self.part_2(self.input)}")


def get_file_path(name: str) -> str:
    script_dir = os.path.dirname(__file__)
    rel_path: str = name + ".txt"
    abs_file_path = os.path.join(script_dir, rel_path)
    return abs_file_path


def load_input(name: str) -> list[str]:
    with open(get_file_path(name), "r") as file:
        return [l for l in file.read().strip().split("\n")]


def multiply(xs: t.Iterable[int]) -> int:
    total = 1
    for x in xs:
        total = total * x
    return total
