import functools

from benchmarks.setup_msgspec import (
    access_struct,
    create_struct,
    equal_struct,
    hash_struct,
    instantiate_struct,
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
    (*bench(create_struct, create_record, 10), "class creation (msgspec struct)"),
    (*bench(instantiate_struct, instantiate_record, 1_000), "instantiation (msgspec struct)"),
    (*bench(access_struct, access_record, 10_000), "attribute access (msgspec struct)"),
    (*bench(equal_struct, equal_record, 10_000), "equality (msgspec struct)"),
    (*bench(hash_struct, hash_record, 1_000), "hashing (msgspec struct)"),
]
