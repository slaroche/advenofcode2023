from adventofcode.utils import Result, multiply


def parse(line: str) -> list[int]:
    _, numbers = line.split(": ")
    return [int(n) for n in numbers.split(" ") if n != ""]


def process(time: int, distance: int) -> int:
    l: int | None = None
    count = 0
    for i in range(time):
        d = i * (time - i)

        if l is None:
            l = d if d > distance else None
        elif d < distance:
            return count

        if d > distance:
            count += 1

    return count


def part_1(input: list[str]) -> int:
    times = parse(input[0])
    distances = parse(input[1])
    total = []
    for i in range(len(times)):
        total.append(process(times[i], distances[i]))
    return multiply(total)


def parse_2(line: str) -> int:
    _, numbers = line.split(": ")
    return int(numbers.replace(" ", ""))


def part_2(input: list[str]) -> int:
    time = parse_2(input[0])
    distance = parse_2(input[1])
    return process(time, distance)


def run(input: list[str]) -> Result:
    return Result(
        input=input,
        part_1=part_1,
        part_2=part_2,
    )
