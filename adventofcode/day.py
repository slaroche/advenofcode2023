import typing as t

import click

from adventofcode import day1, day2, day3
from adventofcode.utils import Result, load_input


class Handler(t.Protocol):
    __name__: str

    def run(self, input: list[str]) -> Result:
        ...


handlers: list[Handler] = [
    day1,
    day2,
    day3,
]


@click.command()
@click.option("--example", "-e", is_flag=True, default=False)
@click.argument("day")
def hello(example: bool, day: str) -> None:
    hander = handlers[int(day) - 1]
    name = hander.__name__.split(".")[-1]
    input = load_input("example_" + name if example else name)

    result: Result = hander.run(
        input=input,
    )
    result.print()


if __name__ == "__main__":
    hello()
