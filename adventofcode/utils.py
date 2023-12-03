import dataclasses
import enum
import os
import typing as t


class Part(enum.IntEnum):
    FIRST = 1
    SECOND = 2


@dataclasses.dataclass
class Result:
    answer_1: int | None = None
    answer_2: int | None = None

    error: str | None = None

    def print(self) -> None:
        if self.error:
            print(f"Error: {self.error}")
            return None

        if self.answer_1:
            print(f"Part one puzzle answer is: {self.answer_1}")
        else:
            print(f"Waiting for part one puzzle answer")
        if self.answer_2:
            print(f"Part two puzzle answer is: {self.answer_2}")


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
