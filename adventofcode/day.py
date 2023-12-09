import importlib
import typing as t

import click

from adventofcode.utils import Result, load_input


class Handler(t.Protocol):
    __name__: str

    def run(self, input: list[str]) -> Result:
        ...


@click.command()
@click.option("--example", "-e", is_flag=True, default=False, help="Run example input.")
@click.option("--input-file", "-i", default="", help="Use specific input file.")
@click.option(
    "--part",
    "-p",
    default="all",
    type=click.Choice(["all", "1", "2"]),
    help="Run specific part.",
)
@click.argument("day")
def hello(example: bool, input_file: str, part: str, day: str) -> None:
    handler: Handler = importlib.import_module("adventofcode.day" + day)
    name = handler.__name__.split(".")[-1]
    input_name = "example" if example else "input"
    input_name = input_file or input_name
    input = load_input(f"{name}/{input_name}")

    result: Result = handler.run(input=input)
    match part:
        case "all":
            result.print_answers()
        case "1":
            result.print_part_1()
        case "2":
            result.print_part_2()


if __name__ == "__main__":
    hello()
