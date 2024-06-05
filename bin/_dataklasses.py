# dataklasses.py
#
#     https://github.com/dabeaz/dataklasses
#
# Author: David Beazley (@dabeaz).
#         http://www.dabeaz.com
#
# Copyright (C) 2021-2022.
#
# Permission is granted to use, copy, and modify this code in any
# manner as long as this copyright message and disclaimer remain in
# the source code.  There is no warranty.  Try to use the code for the
# greater good.

# type: ignore
# ruff: noqa: ANN001, ANN202, S102

__all__ = ["dataklass"]

from functools import lru_cache, reduce


def all_hints(cls: type) -> dict[str, object]:
    """Collect all type hints from a class and base classes."""

    return reduce(lambda x, y: getattr(y, "__annotations__", {}) | x, cls.__mro__, {})


def codegen(func: object):
    @lru_cache
    def make_func_code(numfields: int) -> object:
        names = [f"_{n}" for n in range(numfields)]
        local_ns: dict[str, object] = {}
        exec(func(names), globals(), local_ns)
        return local_ns.popitem()[1]

    return make_func_code


def patch_args_and_attributes(func, fields: dict[str, object], start: int = 0):
    new_func = type(func)(
        func.__code__.replace(
            co_names=(*func.__code__.co_names[:start], *fields),
            co_varnames=("self", *fields),
        ),
        func.__globals__,
    )
    new_func.__annotations__ = dict(fields)
    return new_func


def patch_attributes(func, fields: dict[str, object], start: int = 0):
    new_func = type(func)(func.__code__.replace(co_names=(*func.__code__.co_names[:start], *fields)), func.__globals__)
    new_func.__annotations__ = dict(fields)
    return new_func


@codegen
def make__init__(fields: dict[str, object]) -> str:
    args = ", ".join(fields)
    body = "\n".join(f"   self.{name} = {name}" for name in fields)
    return f"def __init__(self, {args}) -> None:\n{body}\n"


@codegen
def make__repr__(fields: dict[str, object]) -> str:
    fmt = ", ".join(f"{{self.{name}!r}}" for name in fields)
    return f"def __repr__(self) -> str:\n    return f'{{type(self).__name__}}({fmt})'\n"


@codegen
def make__eq__(fields: dict[str, object]) -> str:
    selfvals = ", ".join(f"self.{name}" for name in fields)
    othervals = ", ".join(f"other.{name}" for name in fields)
    return (
        "def __eq__(self, other: object):\n"
        "    if self.__class__ is other.__class__:\n"
        f"        return ({selfvals},) == ({othervals},)\n"
        "    else:\n"
        "        return NotImplemented\n"
    )


def dataklass(cls: type) -> type:
    fields = all_hints(cls)
    nfields = len(fields)
    clsdict = vars(cls)
    if "__init__" not in clsdict:
        cls.__init__ = patch_args_and_attributes(make__init__(nfields), fields)
    if "__repr__" not in clsdict:
        cls.__repr__ = patch_attributes(make__repr__(nfields), fields, 2)
    if "__eq__" not in clsdict:
        cls.__eq__ = patch_attributes(make__eq__(nfields), fields, 1)
    cls.__match_args__ = tuple(fields)
    return cls


# Example use
if __name__ == "__main__":

    @dataklass
    class Coordinates:
        x: int
        y: int
