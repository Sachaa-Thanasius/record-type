import attrs


@attrs.define(frozen=True)
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
