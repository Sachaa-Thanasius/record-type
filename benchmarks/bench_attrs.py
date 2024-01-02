import functools

from benchmarks.setup_attrs import (
    access_attrs_class,
    create_attrs_class,
    equal_attrs_class,
    hash_attrs_class,
    instantiate_attrs_class,
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
    (*bench(create_attrs_class, create_record, 10), "class creation (attrs class)"),
    (*bench(instantiate_attrs_class, instantiate_record, 1_000), "instantiation (attrs class)"),
    (*bench(access_attrs_class, access_record, 10_000), "attribute access (attrs class)"),
    (*bench(equal_attrs_class, equal_record, 10_000), "equality (attrs class)"),
    (*bench(hash_attrs_class, hash_record, 1_000), "hashing (attrs class)"),
]
