# [Advent of Code 2023](https://adventofcode.com/2023)

This project builds with [Poetry](https://python-poetry.org/).

Setup:

```sh
curl -sSL https://install.python-poetry.org | python3 -
poetry install
```

Print solutions for the inputs provided in local data files:

```sh
poetry run day --help
poetry run day 1
poetry run day 2 -e
poetry run day 8 -p 1 -i example_
```

Lint and format code with [Black](https://black.readthedocs.io/), [mypy](https://mypy.readthedocs.io/en/stable/), and [isort](https://pycqa.github.io/isort/):

```sh
make mypy
make format
```
