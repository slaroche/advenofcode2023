from functools import partial

from aoc2023.utils import Handler

digits = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def is_int(value: str) -> bool:
    try:
        int(value)
        return True
    except ValueError:
        return False


def get_digit(line: str, include_spelled_digit: bool = False) -> str | None:
    if is_int(line[0]):
        return line[0]

    if include_spelled_digit:
        for d, v in digits.items():
            if line.startswith(d):
                return str(v)

    return None


def _run(input: list[str], include_spelled_digit: bool = False) -> int:
    total: int = 0
    for line in input:
        values: list[str] = []
        for i in range(len(line)):
            value = get_digit(line[i:], include_spelled_digit=include_spelled_digit)
            if not value:
                continue
            values.append(value)
        if values:
            total += int(values[0] + values[-1])
        else:
            print(f"Error {values}")
    return total


def create_handler(input: list[str]) -> Handler:
    return Handler(
        input=input,
        part_1=partial(_run, include_spelled_digit=False),
        part_2=partial(_run, include_spelled_digit=True),
    )
