"""A import performance test of various types of classes.

Modified from dataklasses: https://github.com/dabeaz/dataklasses/blob/df31f4121dd7938a3933f89008a811dfd0b8520d/perf.py
"""
# ruff: noqa: T201, PTH123

import sys
import time

STANDARD_TEMPLATE = """
class C{n}:
    def __init__(self, a: int, b: int, c: int, d: int, e: int) -> None:
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e

    def __repr__(self) -> str:
        return f'C{n}({{self.a!r}}, {{self.b!r}}, {{self.c!r}}, {{self.d!r}}, {{self.e!r}})'

    def __eq__(self, other) -> bool:
        if self.__class__ is other.__class__:
            return (self.a, self.b, self.c, self.d, self.e) == (other.a, other.b, other.c, other.d, other.e)
        else:
            return NotImplemented
"""

NAMEDTUPLE_TEMPLATE = """
class C{n}(NamedTuple):
    a: int
    b: int
    c: int
    d: int
    e: int
"""

DATACLASS_TEMPLATE = """
@dataclass
class C{n}:
    a: int
    b: int
    c: int
    d: int
    e: int
"""

ATTRS_TEMPLATE = """
@frozen
class C{n}:
    a: int
    b: int
    c: int
    d: int
    e: int
"""

MSGSPEC_TEMPLATE = """
class C{n}(Struct):
    a: int
    b: int
    c: int
    d: int
    e: int
"""

RECORD_TEMPLATE = """
@record
def C{n}(a: int, b: int, c: int, d: int, e: int) -> None:
    ...
"""

CLUEGEN_TEMPLATE = """
class C{n}(Datum):
    a: int
    b: int
    c: int
    d: int
    e: int
"""

DATAKLASS_TEMPLATE = """
@dataklass
class C{n}:
    a: int
    b: int
    c: int
    d: int
    e: int
"""


def run_test(repetitions: int) -> float:
    start = time.perf_counter()

    for _ in range(repetitions):
        import perftemp  # noqa: F401

        del sys.modules["perftemp"]

    end = time.perf_counter()
    return end - start


def write_perftemp(count: int, template: str, setup: str) -> None:
    with open("perftemp.py", "w") as f:
        f.write(setup)
        f.write("\n")
        for n in range(count):
            f.write(template.format(n=n))


def main(repetitions: int = 100) -> None:
    CLASS_COUNT = 100

    # Create the test cases.
    # fmt: off
    test_cases: tuple[str, str, str] = [
        ("standard classes",    STANDARD_TEMPLATE,      ""),
        ("namedtuple",          NAMEDTUPLE_TEMPLATE,    "from typing import NamedTuple"),
        ("dataclasses",         DATACLASS_TEMPLATE,     "from dataclasses import dataclass"),
        ("attrs",               ATTRS_TEMPLATE,         "from attrs import frozen"),
        ("msgspec",             MSGSPEC_TEMPLATE,       "from msgspec import Struct"),
        ("record",              RECORD_TEMPLATE,        "from record_type import record"),
        ("cluegen",             CLUEGEN_TEMPLATE,       "from bin._cluegen import Datum"),
        ("dataklasses",         DATAKLASS_TEMPLATE,     "from bin._dataklasses import dataklass"),
    ]
    # fmt: on

    # Run the tests and collect the results.
    results: dict[str, float] = {}
    for name, template, setup in test_cases:
        write_perftemp(CLASS_COUNT, template, setup)
        try:
            timespan = run_test(repetitions)
        except ImportError:
            print(f"{name} not installed")
        else:
            results[name] = timespan

    sorted_results = sorted(results.items(), key=lambda r: r[1])

    # Pretty-print the results.
    PADDING = 20

    print(f"{f'{CLASS_COUNT} Classes':>{PADDING}} │ Time (s)")
    print(f"{'─' * PADDING}─┼──────────")
    print("\n".join(f"{name:>{PADDING}} │ {timespan:.5f}" for name, timespan in sorted_results))


if __name__ == "__main__":
    repetitions = int(sys.argv[1]) if len(sys.argv) == 2 else 100
    raise SystemExit(main(repetitions))
