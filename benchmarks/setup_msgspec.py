import msgspec


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
