import dataclasses

from aoc2023.utils import Handler


def same_but_one(previous: str, current: str) -> bool:
    return len([i for i, p in enumerate(previous) if p != current[i]]) == 1


def find_h_reflextion(
    lines: list[str], is_same_or_same_but_one: bool = False
) -> int | None:
    previous = ""
    for i, line in enumerate(lines):
        done = False
        is_done = []
        if i == 0:
            previous = line
            continue
        if previous != line:
            if not is_same_or_same_but_one:
                previous = line
                continue
            if not same_but_one(line, previous):
                previous = line
                continue
            is_done.append("is done")
            done = True
        down_cursor = i + 1
        up_cursor = i - 2
        stop = False
        while not stop:
            if down_cursor == len(lines):
                if done:
                    return i
                stop = True
                continue
            if up_cursor == -1 and done:
                if done:
                    return i
                stop = True
                continue

            if lines[down_cursor] != lines[up_cursor]:
                if not is_same_or_same_but_one:
                    stop = True
                    continue
                if not done and not same_but_one(lines[down_cursor], lines[up_cursor]):
                    stop = True
                    continue
                is_done.append("is done")
                done = True
            down_cursor += 1
            up_cursor -= 1
        previous = line

    return None


@dataclasses.dataclass
class Pattern:
    lines: list[str] = dataclasses.field(default_factory=list)
    is_same_or_same_but_one: bool = False

    @property
    def rotated(self) -> list[str]:
        return map("".join, zip(*self.lines))

    def find_reflextion(self) -> int:
        reflextion = self.find_h_reflextion()
        if reflextion:
            return reflextion * 100
        reflextion = self.find_v_reflextion()
        if reflextion:
            return reflextion
        return 0
        # raise ValueError()

    def find_h_reflextion(self) -> int | None:
        reflextion = find_h_reflextion(self.lines, self.is_same_or_same_but_one)
        if reflextion:
            return reflextion
        return None

    def find_v_reflextion(self) -> int | None:
        reflextion = find_h_reflextion(self.rotated, self.is_same_or_same_but_one)
        if reflextion:
            return reflextion
        return None

    def print(self, rotated: bool = False) -> None:
        for i, line in enumerate(self.rotated if rotated else self.lines):
            space = ""
            if i < 10:
                space = " "
            print(i, space + line)


def part_1(input: list[str]) -> int:
    notes = []
    pattern = Pattern()
    for line in input:
        if line == "" or line == "end":
            note = pattern.find_reflextion()
            notes.append(note)
            pattern = Pattern()
            continue
        pattern.lines.append(line)

    return sum(notes)


def part_2(input: list[str]) -> int:
    notes = []
    pattern = Pattern(is_same_or_same_but_one=True)
    for i, line in enumerate(input):
        if line == "" or line == "end":
            note = pattern.find_reflextion()
            notes.append(note)
            pattern = Pattern(is_same_or_same_but_one=True)
            continue
        pattern.lines.append(line)
    return sum(notes)


def create_handler(input: list[str]) -> Handler:
    return Handler(
        input=input,
        part_1=part_1,
        part_2=part_2,
    )
