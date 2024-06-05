from collections.abc import Callable
from typing import Any, ClassVar, Generic, TypeVar, dataclass_transform, type_check_only

_DatumT = TypeVar("_DatumT", bound=DatumBase)

@type_check_only
class _ClueGenDescriptor(Generic[_DatumT]):
    def __get__(self, instance: _DatumT, owner: type[_DatumT]) -> Any: ...
    def __set_name__(self, owner: type[_DatumT], name: str) -> None: ...

def all_clues(cls: type) -> dict[str, Any]: ...
def cluegen(func: Callable[[type[_DatumT]], str]) -> _ClueGenDescriptor[_DatumT]: ...

class DatumBase:
    __slots__ = ()
    _methods: ClassVar[list[tuple[str, Any]]] = []

@dataclass_transform()
class Datum(DatumBase):
    __slots__ = ()
