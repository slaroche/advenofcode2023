import dataclasses
import math
import typing as t

from aoc2023.utils import Handler


@dataclasses.dataclass
class Node:
    id: str
    left: str
    right: str
    mapping: dict[str, "Node"] = dataclasses.field(default_factory=dict)

    @classmethod
    def parse(cls, line: str) -> t.Self:
        id_, rest = line.split("=")
        left, right = rest.replace("(", "").replace(")", "").replace(" ", "").split(",")
        return cls(
            id=id_.replace(" ", ""),
            left=left,
            right=right,
        )

    def populate(self, nodes: dict[str, "Node"]) -> None:
        self.mapping["L"] = nodes[self.left]
        self.mapping["R"] = nodes[self.right]

    def goto(self, i: str) -> "Node":
        return self.mapping[i]

    def __repr__(self) -> str:
        return f"{self.id} = ({self.right}, {self.left})"


def part_1(input: list[str]) -> int:
    nodes: dict[str, Node] = {}
    instruction = ""
    position: Node | None = None
    for i, line in enumerate(input):
        if i == 0:
            instruction = line
            continue

        if i == 1:
            continue

        node = Node.parse(line)
        nodes[node.id] = node
        if node.id == "AAA":
            position = node

    for node in nodes.values():
        node.populate(nodes)

    count = 0
    if not position:
        return count

    stop = False
    while True:
        for instr in instruction:
            count += 1
            position = position.goto(instr)

            if position.id == "ZZZ":
                stop = True
                break
        if stop:
            break

    return count


def lcm(v: list[int]) -> int:
    if len(v) == 1:
        return v[0]
    a = v[0]
    b = v[1]
    return lcm([abs(a * b) // math.gcd(a, b)] + [n for n in v[2:]])


def part_2(input: list[str]) -> int:
    nodes: dict[str, Node] = {}
    instruction = ""
    positions: list[Node] = []
    for i, line in enumerate(input):
        if i == 0:
            instruction = line
            continue

        if i == 1:
            continue

        node = Node.parse(line)
        nodes[node.id] = node
        if node.id.endswith("A"):
            positions.append(node)

    for node in nodes.values():
        node.populate(nodes)

    counts = []

    for position in positions:
        count = 0
        continue_ = True
        p = dataclasses.replace(position)

        while continue_:
            for instr in instruction:
                count += 1
                p = p.goto(instr)

                if p.id.endswith("Z"):
                    continue_ = False
                    counts.append(count)
                    break

    return lcm(counts)


def create_handler(input: list[str]) -> Handler:
    return Handler(
        input=input,
        part_1=part_1,
        part_2=part_2,
    )
