import dataclasses

from aoc2023.utils import Handler


def same_but_one(previous: str, current: str) -> bool:
    return len([i for i, p in enumerate(previous) if p != current[i]]) == 1


@dataclasses.dataclass
class CompareHander:
    mut_is_smudge_fixed: bool

    def is_equal(self, previous: str, current: str) -> bool:
        if self.mut_is_smudge_fixed or previous == current:
            return previous == current
        self.mut_is_smudge_fixed = same_but_one(previous, current)
        return self.mut_is_smudge_fixed


def find_h_reflextion(lines: list[str], is_same_but_one: bool = False) -> int | None:
    for i, _ in enumerate(lines[1:-1]):
        i = i + 1
        max_iter = min(i, len(lines) - i - 1)
        compare_handler = CompareHander(False)
        is_equal = (
            lambda a, b: compare_handler.is_equal(a, b) if is_same_but_one else a == b
        )
        to_compare = zip(lines[i : i + max_iter], reversed(lines[i - max_iter : i]))
        if (
            not all(is_equal(down, up) for down, up in to_compare)
            and not compare_handler.mut_is_smudge_fixed
        ):
            continue

        return i
    return None


@dataclasses.dataclass
class Pattern:
    lines: list[str] = dataclasses.field(default_factory=list)

    @property
    def rotated(self) -> list[str]:
        return list(map("".join, zip(*self.lines)))

    def find_reflextion(self, is_same_but_one: bool = False) -> int:
        reflextion = self.find_h_reflextion(is_same_but_one)
        if reflextion:
            return reflextion * 100
        reflextion = self.find_v_reflextion(is_same_but_one)
        if reflextion:
            return reflextion
        return 0
        # raise ValueError()

    def find_h_reflextion(self, is_same_but_one: bool = False) -> int | None:
        reflextion = find_h_reflextion(self.lines, is_same_but_one)
        if reflextion:
            return reflextion
        return None

    def find_v_reflextion(self, is_same_but_one: bool = False) -> int | None:
        reflextion = find_h_reflextion(self.rotated, is_same_but_one)
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
    pattern = Pattern()
    for i, line in enumerate(input):
        if line == "" or line == "end":
            note = pattern.find_reflextion(is_same_but_one=True)
            notes.append(note)
            pattern = Pattern()
            continue
        pattern.lines.append(line)
    return sum(notes)


def create_handler(input: list[str]) -> Handler:
    return Handler(
        input=input,
        part_1=part_1,
        part_2=part_2,
    )
