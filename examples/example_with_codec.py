# coding: record

record ExampleRecord(a: int, b: str, *, c: float = 1.0):
    """ExampleRecord docstring."""

thing = ExampleRecord(1, "2")
print(repr(thing))