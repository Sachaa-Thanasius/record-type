# ruff: noqa: B015, B018, PLR0124
import dataclasses
import functools
import typing

import attrs
import msgspec

import record_type

# ================================
# ==== records
# ================================


@record_type.record
def Point3DRecord(x: float, y: float, z: float):
    """A point in 3D space."""


point_3D_record = Point3DRecord(1.0, 2.0, 3.0)


def create_record(num_iterations: int):
    for _ in range(num_iterations):

        @record_type.record
        def Point3D(x: float, y: float, z: float):
            """A point in 3D space."""


def instantiate_record(num_iterations: int):
    for _ in range(num_iterations):
        Point3DRecord(1.0, 2.0, 3.0)


def access_record(num_iterations: int):
    for _ in range(num_iterations):
        point_3D_record.x
        point_3D_record.y
        point_3D_record.z


def equal_record(num_iterations: int):
    for _ in range(num_iterations):
        point_3D_record == point_3D_record


def hash_record(num_iterations: int):
    for _ in range(num_iterations):
        hash(point_3D_record)


# ================================
# ==== standard classes
# ================================


class Point3DClass:
    """A point in 3D space."""

    __slots__ = ("_record_cached_repr", "_record_cached_hash", "x", "y", "z")
    __match_args__ = ("x", "y", "z")

    x: float
    y: float
    z: float

    def __init__(self, x: float, y: float, z: float) -> None:
        object.__setattr__(self, "x", x)
        object.__setattr__(self, "y", y)
        object.__setattr__(self, "z", z)

    def __repr__(self) -> str:
        try:
            return self._record_cached_repr
        except AttributeError:
            object.__setattr__(
                self, "_record_cached_repr", f"{type(self).__name__}({self.x!r}, {self.y!r}, {self.z!r})"
            )
            return self._record_cached_repr

    def __setattr__(self, name: str, value: object, /) -> typing.NoReturn:
        msg = f"{type(self).__name__} is immutable."
        raise AttributeError(msg)

    def __delattr__(self, name: str, /) -> typing.NoReturn:
        msg = f"{type(self).__name__} is immutable."
        raise AttributeError(msg)

    def __eq__(self, other: object, /) -> bool:
        other_slots: tuple[str, ...] | list[object] = getattr(type(other), "__slots__", [object()])
        self_slots = type(self).__slots__
        if id(other_slots) == id(self_slots):
            return True

        other_attrs = frozenset(other_slots)
        self_attrs = frozenset(self_slots)
        if self_attrs != other_attrs:
            # Avoids the question of what to do if there are extra attributes on
            # `other`.
            return NotImplemented

        for attr in self_attrs:
            if not hasattr(other, attr):
                return NotImplemented
            # fmt: off
            if (
                attr not in {"_record_cached_hash", "_record_cached_repr"}
                and getattr(self, attr) != getattr(other, attr)
            ):
                return False
            # fmt: on
        return True

    def __hash__(self) -> int:
        try:
            return self._record_cached_hash
        except AttributeError:
            object.__setattr__(self, "_record_cached_hash", hash((self.x, self.y, self.z)))
            return self._record_cached_hash


point_3D_standard = Point3DClass(1.0, 2.0, 3.0)


def create_standard(num_iterations: int):
    for _ in range(num_iterations):

        class Point3DClass:
            """A point in 3D space."""

            __slots__ = ("x", "y", "z")
            __match_args__ = ("x", "y", "z")

            x: float
            y: float
            z: float

            def __init__(self, x: float, y: float, z: float) -> None:
                object.__setattr__(self, "x", x)
                object.__setattr__(self, "y", y)
                object.__setattr__(self, "z", z)

            def __repr__(self) -> str:
                return f"{type(self).__name__}({self.x!r}, {self.y!r}, {self.z!r})"

            def __setattr__(self, name: str, value: object, /):
                msg = f"{type(self).__name__} is immutable."
                raise AttributeError(msg)

            def __delattr__(self, name: str, /):
                msg = f"{type(self).__name__} is immutable."
                raise AttributeError(msg)

            def __eq__(self, other: object, /) -> bool:
                other_slots: tuple[str, ...] | list[object] = getattr(type(other), "__slots__", [object()])
                self_slots = type(self).__slots__
                if id(other_slots) == id(self_slots):
                    return True

                other_attrs = frozenset(other_slots)
                self_attrs = frozenset(self_slots)
                if self_attrs != other_attrs:
                    # Avoids the question of what to do if there are extra attributes on
                    # `other`.
                    return NotImplemented

                for attr in self_attrs:
                    if not hasattr(other, attr):
                        return NotImplemented
                    if attr not in {"_record_cached_hash", "_record_cached_repr"} and getattr(self, attr) != getattr(
                        other, attr
                    ):
                        return False
                return True

            def __hash__(self) -> int:
                try:
                    return self._record_cached_hash
                except AttributeError:
                    object.__setattr__(self, "_record_cached_hash", hash((self.x, self.y, self.z)))
                    return self._record_cached_hash


def instantiate_standard(num_iterations: int):
    for _ in range(num_iterations):
        Point3DClass(1.0, 2.0, 3.0)


def access_standard(num_iterations: int):
    for _ in range(num_iterations):
        point_3D_standard.x
        point_3D_standard.y
        point_3D_standard.z


def equal_standard(num_iterations: int):
    for _ in range(num_iterations):
        point_3D_standard == point_3D_standard


def hash_standard(num_iterations: int):
    for _ in range(num_iterations):
        hash(point_3D_standard)


# ================================
# ==== named tuples
# ================================


class Point3DNamedTuple(typing.NamedTuple):
    """A point in 3D space."""

    x: float
    y: float
    z: float


point_3D_namedtuple = Point3DNamedTuple(1.0, 2.0, 3.0)


def create_namedtuple(num_iterations: int):
    for _ in range(num_iterations):

        class Point3D(typing.NamedTuple):
            """A point in 3D space."""

            x: float
            y: float
            z: float


def instantiate_namedtuple(num_iterations: int):
    for _ in range(num_iterations):
        Point3DNamedTuple(1.0, 2.0, 3.0)


def access_namedtuple(num_iterations: int):
    for _ in range(num_iterations):
        point_3D_namedtuple.x
        point_3D_namedtuple.y
        point_3D_namedtuple.z


def equal_namedtuple(num_iterations: int):
    for _ in range(num_iterations):
        point_3D_namedtuple == point_3D_namedtuple


def hash_namedtuple(num_iterations: int):
    for _ in range(num_iterations):
        hash(point_3D_namedtuple)


# ================================
# ==== dataclasses
# ================================


@dataclasses.dataclass(frozen=True, slots=True, match_args=True)
class Point3DDataclass:
    """A point in 3D space."""

    x: float
    y: float
    z: float


point_3D_dataclass = Point3DDataclass(1.0, 2.0, 3.0)


def create_dataclass(num_iterations: int):
    for _ in range(num_iterations):

        @dataclasses.dataclass(frozen=True, slots=True)
        class Point3D:
            """A point in 3D space."""

            x: float
            y: float
            z: float


def instantiate_dataclass(num_iterations: int):
    for _ in range(num_iterations):
        Point3DDataclass(1.0, 2.0, 3.0)


def access_dataclass(num_iterations: int):
    for _ in range(num_iterations):
        point_3D_dataclass.x
        point_3D_dataclass.y
        point_3D_dataclass.z


def equal_dataclass(num_iterations: int):
    for _ in range(num_iterations):
        point_3D_dataclass == point_3D_dataclass


def hash_dataclass(num_iterations: int):
    for _ in range(num_iterations):
        hash(point_3D_dataclass)


# ================================
# ==== attrs classes
# ================================


@attrs.define(frozen=True, slots=True, match_args=True)
class Point3DAttrsClass:
    """A point in 3D space."""

    x: float
    y: float
    z: float


point_3D_attrs_class = Point3DAttrsClass(1.0, 2.0, 3.0)


def create_attrs_class(num_iterations: int):
    for _ in range(num_iterations):

        @attrs.define(frozen=True)
        class Point3D:
            """A point in 3D space."""

            x: float
            y: float
            z: float


def instantiate_attrs_class(num_iterations: int):
    for _ in range(num_iterations):
        Point3DAttrsClass(1.0, 2.0, 3.0)


def access_attrs_class(num_iterations: int):
    for _ in range(num_iterations):
        point_3D_attrs_class.x
        point_3D_attrs_class.y
        point_3D_attrs_class.z


def equal_attrs_class(num_iterations: int):
    for _ in range(num_iterations):
        point_3D_attrs_class == point_3D_attrs_class


def hash_attrs_class(num_iterations: int):
    for _ in range(num_iterations):
        hash(point_3D_attrs_class)


# ================================
# ==== msgspec structs
# ================================


class Point3DStruct(msgspec.Struct, frozen=True):
    """A point in 3D space."""

    x: float
    y: float
    z: float


point_3D_struct = Point3DStruct(1.0, 2.0, 3.0)


def create_struct(num_iterations: int):
    for _ in range(num_iterations):

        class Point3D(msgspec.Struct, frozen=True):
            """A point in 3D space."""

            x: float
            y: float
            z: float


def instantiate_struct(num_iterations: int):
    for _ in range(num_iterations):
        Point3DStruct(1.0, 2.0, 3.0)


def access_struct(num_iterations: int):
    for _ in range(num_iterations):
        point_3D_struct.x
        point_3D_struct.y
        point_3D_struct.z


def equal_struct(num_iterations: int):
    for _ in range(num_iterations):
        point_3D_struct == point_3D_struct


def hash_struct(num_iterations: int):
    for _ in range(num_iterations):
        hash(point_3D_struct)


# ================================
# ==== benchmark cases
# ================================


def bench(func1, func2, num_iterations: int) -> functools.partial[None]:
    return (functools.partial(func1, num_iterations), functools.partial(func2, num_iterations))


# fmt: off
CREATE_NUM = 10
INST_NUM   = 1_000
ACCESS_NUM = 10_000
EQUAL_NUM  = 10_000
HASH_NUM   = 1_000
# fmt: on

# fmt: off
__benchmarks__ = [
    # standard classes
    (*bench(create_record, create_standard, CREATE_NUM),            "(class)   class creation"),
    (*bench(instantiate_record, instantiate_standard, INST_NUM),    "(class)    instantiation"),
    (*bench(access_record, access_standard, ACCESS_NUM),            "(class) attribute access"),
    (*bench(equal_record, equal_standard, EQUAL_NUM),               "(class)         equality"),
    (*bench(hash_record, hash_standard, HASH_NUM),                  "(class)          hashing"),
    # named tuples
    (*bench(create_record, create_namedtuple, CREATE_NUM),          "(namedtuple)   class creation"),
    (*bench(instantiate_record, instantiate_namedtuple, INST_NUM),  "(namedtuple)    instantiation"),
    (*bench(access_record, access_namedtuple, ACCESS_NUM),          "(namedtuple) attribute access"),
    (*bench(equal_record, equal_namedtuple, EQUAL_NUM),             "(namedtuple)         equality"),
    (*bench(hash_record, hash_namedtuple, HASH_NUM),                "(namedtuple)          hashing"),
    # dataclasses
    (*bench(create_record, create_dataclass, CREATE_NUM),           "(dataclass)   class creation"),
    (*bench(instantiate_record, instantiate_dataclass, INST_NUM),   "(dataclass)    instantiation"),
    (*bench(access_record, access_dataclass, ACCESS_NUM),           "(dataclass) attribute access"),
    (*bench(equal_record, equal_dataclass, EQUAL_NUM),              "(dataclass)         equality"),
    (*bench(hash_record, hash_dataclass, HASH_NUM),                 "(dataclass)          hashing"),
    # attrs classes
    (*bench(create_record, create_attrs_class, CREATE_NUM),         "(attrs class)   class creation"),
    (*bench(instantiate_record, instantiate_attrs_class, INST_NUM), "(attrs class)    instantiation"),
    (*bench(access_record, access_attrs_class, ACCESS_NUM),         "(attrs class) attribute access"),
    (*bench(equal_record, equal_attrs_class, EQUAL_NUM),            "(attrs class)         equality"),
    (*bench(hash_record, hash_attrs_class, HASH_NUM),               "(attrs class)          hashing"),
    # msgspec structs
    (*bench(create_record, create_struct, CREATE_NUM),              "(msgspec struct)   class creation"),
    (*bench(instantiate_record, instantiate_struct, INST_NUM),      "(msgspec struct)    instantiation"),
    (*bench(access_record, access_struct, ACCESS_NUM),              "(msgspec struct) attribute access"),
    (*bench(equal_record, equal_struct, EQUAL_NUM),                 "(msgspec struct)         equality"),
    (*bench(hash_record, hash_struct, HASH_NUM),                    "(msgspec struct)          hashing"),
]
# fmt: on
