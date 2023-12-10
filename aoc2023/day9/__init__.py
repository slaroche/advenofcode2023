import dataclasses
import pprint
import typing as t
from collections import UserList
from functools import partial

from aoc2023.utils import Handler


@dataclasses.dataclass(init=False, repr=False)
class Sequence(UserList[int]):
    _reverse: bool = False

    def fill_placeholder(self, step: int) -> None:
        value: int = self.data[-1]
        if self._reverse:
            value -= step
        else:
            value += step
        self.data.append(value)

    def reverse(self) -> None:
        super().reverse()
        self._reverse = True


def seq_factory(line: str) -> Sequence:
    return Sequence([int(x) for x in line.split(" ")])


def _run(input: list[str], reverse: bool) -> int:
    total = 0
    for line in input:
        sequences: list[Sequence] = [seq_factory(line)]
        while True:
            new_seq = Sequence()
            seq = sequences[-1]
            for i, value in enumerate(seq):
                if i == len(seq) - 1:
                    break
                new_seq.append(seq[i + 1] - value)

            if reverse:
                seq.reverse()

            sequences.append(new_seq)

            if all(x == 0 for x in new_seq):
                break

        sequences.reverse()
        for i, seq in enumerate(sequences):
            if i == len(sequences) - 1:
                total += seq[-1]
                break
            sequences[i + 1].fill_placeholder(step=seq[-1])

    return total


def create_handler(input: list[str]) -> Handler:
    return Handler(
        input=input,
        part_1=partial(_run, reverse=False),
        part_2=partial(_run, reverse=True),
    )
