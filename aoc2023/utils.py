import contextlib
import dataclasses
import os
import sys
import typing as t

PuzzleFn: t.TypeAlias = t.Callable[[list[str]], int]


class NamedModule(t.Protocol):
    __name__: str


@dataclasses.dataclass
class Handler:
    input: list[str]
    part_1: PuzzleFn
    part_2: PuzzleFn
    block_prints: bool = False

    # Disable
    @contextlib.contextmanager
    def print_context(self) -> t.Iterator[None]:
        if self.block_prints:
            sys.stdout = open(os.devnull, "w")
        yield
        if self.block_prints:
            sys.stdout = sys.__stdout__

    def print_answers(self) -> None:
        self.print_part_1()
        self.print_part_2()

    def print_part_1(self) -> None:
        print(f"Part 1 answer: {self.answer_part_1()}")

    def print_part_2(self) -> None:
        print(f"Part 2 answer: {self.answer_part_2()}")

    def answer_part_1(self) -> int:
        with self.print_context():
            return self.part_1(self.input)

    def answer_part_2(self) -> int:
        with self.print_context():
            return self.part_2(self.input)


class DayModule(t.Protocol):
    __name__: str

    def create_handler(self, input: list[str]) -> Handler:
        ...


def get_module_name(module: NamedModule) -> str:
    return module.__name__.split(".")[-1]


def get_file_path(rel_path: str) -> str:
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, rel_path)
    return abs_file_path


def load_input(
    module: DayModule,
    *,
    file_name: str | None = None,
    example: bool = False,
) -> list[str]:
    name = get_module_name(module)
    default_file_name = "example" if example else "input"
    file_name = file_name or f"{default_file_name}.txt"
    rel_path = f"{name}/{file_name}"
    with open(get_file_path(rel_path), "r") as file:
        return [l for l in file.read().strip().split("\n")]


def multiply(xs: t.Iterable[int]) -> int:
    total = 1
    for x in xs:
        total = total * x
    return total
