from functools import partial

from aoc2023.utils import Handler


def is_empty(lines: list[str], *, col: int | None = None, row: int | None = None) -> bool:
    if row is not None:
        return all(x != "#" for x in lines[row])
    if col is not None:
        return all(x[col] != "#" for x in lines)
    raise ValueError()


def run(input: list[str], multiplier: int) -> int:
    galaxies: list[tuple[int, int, int, int]] = []

    total = 0
    empty_row_count = 0
    for i, line in enumerate(input):
        if is_empty(input, row=i):
            empty_row_count += 1
            continue

        empty_col_count = 0
        for j, x in enumerate(line):
            if is_empty(input, col=j):
                empty_col_count += 1
                continue

            if x == "#":
                galaxies.append((empty_row_count, i, empty_col_count, j))

    for i, galaxy in enumerate(galaxies):
        for pair in galaxies[i:]:
            total += (
                max(
                    galaxy[1] + (galaxy[0] * multiplier), pair[1] + (pair[0] * multiplier)
                )
                - min(
                    galaxy[1] + (galaxy[0] * multiplier), pair[1] + (pair[0] * multiplier)
                )
            ) + (
                max(
                    galaxy[3] + (galaxy[2] * multiplier), pair[3] + (pair[2] * multiplier)
                )
                - min(
                    galaxy[3] + (galaxy[2] * multiplier), pair[3] + (pair[2] * multiplier)
                )
            )

    return total


def create_handler(input: list[str]) -> Handler:
    return Handler(
        input=input,
        part_1=partial(run, multiplier=1),
        part_2=partial(run, multiplier=1000000 - 1),
    )
