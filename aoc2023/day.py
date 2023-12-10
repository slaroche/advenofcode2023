import importlib

import click

from aoc2023.utils import DayModule
from aoc2023.utils import Handler
from aoc2023.utils import load_input


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
@click.argument("day", type=click.Choice([str(x) for x in range(1, 25)]))
def main(example: bool, input_file: str, part: str, day: str) -> None:
    module: DayModule = importlib.import_module(f"{__name__}{day}")
    input = load_input(module, file_name=input_file or None, example=example)

    handler: Handler = module.create_handler(input=input)
    match part:
        case "all":
            handler.print_answers()
        case "1":
            handler.print_part_1()
        case "2":
            handler.print_part_2()


if __name__ == "__main__":
    main()
