import inspect
import typing

import record_type

T = typing.TypeVar("T")
U = typing.TypeVar("U")


@record_type.record
def Smaller(a: T, /, b: T, *, c: T) -> None:
    ...


@record_type.record
def Example(a: T, /, b: T, c: T | float = 3.0, *d: bool, e: U, f: dict[U, T], **g: tuple[T, U]) -> None:
    """An example record."""


typing.reveal_type(Smaller)
small1 = Smaller(1, 2, c=3)

ex1 = Example()
typing.reveal_type(ex1)

print(inspect.signature(Smaller.__init__))
