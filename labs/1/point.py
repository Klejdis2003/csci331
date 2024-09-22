import math


class Point3d:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.validate_points()

    def validate_points(self):
        if not isinstance(self.x, (int, float)) or not isinstance(self.y, (int, float)) or not isinstance(self.z, (int, float)):
            raise ValueError("Points must be numbers.")

    def __str__(self):
        return f"{self.x} {self.y} {self.z}"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def distance_from(self, other, x_coefficient=1, y_coefficient=1, z_coefficient=1):
        """
        Calculates the distance between two points in 3D space using the Euclidean distance formula.
        :param other: The other point to calculate the distance from.
        :param x_coefficient: The coefficient to multiply the x distance by.
        :param y_coefficient: The coefficient to multiply the y distance by.
        :param z_coefficient: The coefficient to multiply the z distance by.
        :return: The distance between the two points.
        """
        dx, dy, dz = ((self.x - other.x) * x_coefficient,
                      (self.y - other.y) * y_coefficient,
                      (self.z - other.z) * z_coefficient)
        return math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __lt__(self, other):
        return self.z < other.z

    def __gt__(self, other):
        return self.z > other.z