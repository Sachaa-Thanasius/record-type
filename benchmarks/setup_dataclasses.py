import dataclasses


@dataclasses.dataclass(frozen=True, slots=True)
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
