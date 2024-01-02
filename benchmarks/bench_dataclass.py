import functools

from benchmarks.setup_dataclasses import (
    access_dataclass,
    create_dataclass,
    equal_dataclass,
    hash_dataclass,
    instantiate_dataclass,
)
from benchmarks.setup_records import (
    access_record,
    create_record,
    equal_record,
    hash_record,
    instantiate_record,
)


def bench(func1, func2, num_iterations: int) -> functools.partial[None]:
    return (functools.partial(func1, num_iterations), functools.partial(func2, num_iterations))


__benchmarks__ = [
    (*bench(create_dataclass, create_record, 10), "class creation (dataclass)"),
    (*bench(instantiate_dataclass, instantiate_record, 1_000), "instantiation (dataclass)"),
    (*bench(access_dataclass, access_record, 10_000), "attribute access (dataclass)"),
    (*bench(equal_dataclass, equal_record, 10_000), "equality (dataclass)"),
    (*bench(hash_dataclass, hash_record, 1_000), "hashing (dataclass)"),
]
