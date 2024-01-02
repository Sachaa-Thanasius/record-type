import typing


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
