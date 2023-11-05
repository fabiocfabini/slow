# Slow Programming Language

## Motivation

It's slow cause it's in python. It's in python since I am using it to learn more about compilers and less about C/C++. Objective is from AST do all of the following:

- AST interpreter
- Bytecode lowering and execution
- Compiled (to x86-64 assembly as a first step)
- Try to self host

## Quick start

One needs to have a python with `poetry` installed. Simply run

```console
pip install poetry
```

To install all dependencies

```console
poetry install && poetry shell
```

## Testing

To run available test run:

```console
pytest
```
