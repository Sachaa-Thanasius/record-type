import functools

from .setup_namedtuples import (
    access_namedtuple,
    create_namedtuple,
    equal_namedtuple,
    hash_namedtuple,
    instantiate_namedtuple,
)
from .setup_records import (
    access_record,
    create_record,
    equal_record,
    hash_record,
    instantiate_record,
)


def bench(func1, func2, num_iterations: int) -> functools.partial[None]:
    return (functools.partial(func1, num_iterations), functools.partial(func2, num_iterations))


__benchmarks__ = [
    (*bench(create_namedtuple, create_record, 1), "class creation (namedtuple)"),
    (*bench(instantiate_namedtuple, instantiate_record, 1_000), "instantiation (namedtuple)"),
    (*bench(access_namedtuple, access_record, 10_000), "attribute access (namedtuple)"),
    (*bench(equal_namedtuple, equal_record, 1_000), "equality (namedtuple)"),
    (*bench(hash_namedtuple, hash_record, 1_000), "hashing (namedtuple)"),
]
