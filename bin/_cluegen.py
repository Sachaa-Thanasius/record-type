# cluegen.py
#
# Classes generated from type clues.
#
#     https://github.com/dabeaz/cluegen
#
# Author: David Beazley (@dabeaz).
#         http://www.dabeaz.com
#
# Copyright (C) 2018-2021.
#
# Permission is granted to use, copy, and modify this code in any
# manner as long as this copyright message and disclaimer remain in
# the source code.  There is no warranty.  Try to use the code for the
# greater good.

# type: ignore
# ruff: noqa

import types
from functools import reduce


def all_clues(cls: type) -> dict[str, object]:
    """Collect all type clues from a class and base classes."""

    return reduce(lambda x, y: getattr(y, "__annotations__", {}) | x, cls.__mro__, {})


def cluegen(func) -> object:
    """Decorator to define methods of a class as a code generator."""

    def __get__(self: object, instance: object, cls: type) -> object:
        local_ns: dict[str, object] = {}
        code = func(cls)
        exec(code, local_ns)  # noqa: S102
        meth = local_ns[func.__name__]
        setattr(cls, func.__name__, meth)
        return meth.__get__(instance, cls)

    def __set_name__(self: object, cls: type, name: str) -> None:
        try:
            methods = cls.__dict__["_methods"]
        except KeyError:  # This error indicates _methods is coming from a superclass.
            cls._methods = methods = list(cls._methods)

        methods.append((name, self))

    return type(f"ClueGen_{func.__name__}", (), {"__get__": __get__, "__set_name__": __set_name__})()


class DatumBase:
    """Base class for defining data structures"""

    __slots__ = ()
    _methods = []

    @classmethod
    def __init_subclass__(cls) -> None:
        submethods: list[tuple[str, object]] = []
        for name, val in cls._methods:
            if name not in cls.__dict__:
                setattr(cls, name, val)
                submethods.append((name, val))
            elif val is cls.__dict__[name]:
                submethods.append((name, val))

        if submethods != cls._methods:
            cls._methods = submethods


class Datum(DatumBase):
    __slots__ = ()

    @classmethod
    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        cls.__match_args__ = tuple(all_clues(cls))

    @cluegen
    def __init__(cls) -> str:
        clues = all_clues(cls)
        args = ", ".join(
            f"{name}={getattr(cls, name)!r}"
            if hasattr(cls, name) and not isinstance(getattr(cls, name), types.MemberDescriptorType)
            else name
            for name in clues
        )
        body = "\n".join(f"   self.{name} = {name}" for name in clues)
        return f"def __init__(self, {args}) -> None:\n{body}\n"  # noqa: PLE0101

    @cluegen
    def __repr__(cls) -> str:
        clues = all_clues(cls)
        fmt = ", ".join(f"{name}={{self.{name}!r}}" for name in clues)
        return f"def __repr__(self) -> str:\n    return f'{{type(self).__name__}}({fmt})'"

    @cluegen
    def __eq__(cls) -> str:
        clues = all_clues(cls)
        selfvals = ", ".join(f"self.{name}" for name in clues)
        othervals = ", ".join(f"other.{name}" for name in clues)
        return (
            "def __eq__(self, other: object) -> bool:\n"
            "    if self.__class__ is other.__class__:\n"
            f"        return ({selfvals},) == ({othervals},)\n"
            "    else:\n"
            "        return NotImplemented\n"
        )

    @cluegen
    def __hash__(cls) -> str:
        clues = all_clues(cls)
        self_tuple = f"({', '.join(f'self.{name}' for name in clues)},)" if clues else "()"
        return f"def __hash__(self) -> int:\n    return hash({self_tuple})\n"


# Example use
if __name__ == "__main__":

    class Coordinates(Datum):
        x: int
        y: int
