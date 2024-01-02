import record


@record.record
def Point3DRecord(x: float, y: float, z: float):
    """A point in 3D space."""


point_3D_record = Point3DRecord(1.0, 2.0, 3.0)


def create_record(num_iterations: int):
    for _ in range(num_iterations):

        @record.record
        def Point3D(x: float, y: float, z: float):
            """A point in 3D space."""


def instantiate_record(num_iterations: int):
    for _ in range(num_iterations):
        Point3DRecord(1.0, 2.0, 3.0)


def access_record(num_iterations: int):
    for _ in range(num_iterations):
        point_3D_record.x
        point_3D_record.y
        point_3D_record.z


def equal_record(num_iterations: int):
    for _ in range(num_iterations):
        point_3D_record == point_3D_record


def hash_record(num_iterations: int):
    for _ in range(num_iterations):
        hash(point_3D_record)
