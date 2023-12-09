from collections import defaultdict

from adventofcode.utils import Result


def parse_seeds(line: str) -> list[int]:
    _, numbers = line.split(":", 1)
    return [int(n) for n in numbers.split(" ") if n != ""]


def part_1(input: list[str]) -> int:
    src: list[int] = []
    dest: list[int] = []
    map: dict[tuple[int, int], int] = {}

    for i, line in enumerate(input):
        if i == 0:
            dest = parse_seeds(line)
            continue

        if i == 1:
            continue

        if line == "" or line == "end":
            src = dest.copy()
            dest = []
            for s in src:
                d = None
                for b, dmap in map.items():
                    l, u = b
                    if l <= s < u:
                        d = dmap + (s - l)
                dest.append(d or s)
            continue

        if line[0].isalpha():
            map = {}
            continue

        d, s_str, r = line.split(" ")
        s = int(s_str)
        d = int(d)
        r = int(r)
        map[(s, s + r)] = d

    return min(dest)


def parse_seed_ranges(line: str) -> list[tuple[int, int]]:
    _, numbers = line.split(":", 1)
    seed_ranged = [int(n) for n in numbers.split(" ") if n != ""]
    seeds = []
    s = 0
    for i, r in enumerate(seed_ranged):
        if i % 2:
            seeds.append((s, r))
        else:
            s = r
    return seeds


def process(
    seeds: tuple[int, int], src: tuple[int, int], dest: int
) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
    rest = []
    diff = dest - src[0]
    l = max(src[0], seeds[0])
    u = min(src[0] + src[1], seeds[0] + seeds[1])
    if l > u:
        return [], []
    if seeds[0] < l:
        rest.append((seeds[0], l - seeds[0]))
    if seeds[0] + seeds[1] > u:
        rest.append(
            (
                seeds[0] + seeds[1] + 1,
                seeds[0] + seeds[1] - u,
            )
        )
    return [(l + diff, u - l)], rest


def part_2(input: list[str]) -> int:
    src: list[tuple[int, int]] = []
    dest: list[tuple[int, int]] = []

    map: dict[tuple[int, int], int] = {}

    for i, line in enumerate(input):
        if i == 0:
            dest = parse_seed_ranges(line)
            continue

        if i == 1:
            continue

        if line == "" or line == "end":
            src = dest.copy()
            dest = []
            print("src", src)
            while src:
                seeds = src.pop()
                add_to_dest = True
                for bounds, d in map.items():
                    d, rest = process(seeds=seeds, src=bounds, dest=d)
                    dest.extend(d)
                    src.extend(rest)
                    print("process", seeds, bounds, d, rest)
                    print("src", src)
                    if rest:
                        add_to_dest = False
                    if d and not rest:
                        add_to_dest = False
                if add_to_dest:
                    dest.append(seeds)
            breakpoint()
            continue

        if line[0].isalpha():
            map = {}
            continue

        d, s, r = line.split(" ")
        s = int(s)
        d = int(d)
        r = int(r)
        map[(s, r)] = d

    return min(d for d, _ in dest)


def run(input: list[str]) -> Result:
    return Result(
        input=input,
        part_1=part_1,
        part_2=part_2,
    )
