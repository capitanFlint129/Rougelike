class Coordinates:
    """
    A class to represent coordinates in 2D space.

    Attributes:
        x (int): The x-coordinate of the point.
        y (int): The y-coordinate of the point.
    """

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        if isinstance(other, Coordinates):
            return self.x == other.x and self.y == other.y
        elif isinstance(other, tuple) and len(other) == 2:
            return self.x == other[0] and self.y == other[1]
        return False

    def __iter__(self):
        yield self.x
        yield self.y

    def distance(self, other):
        """
        Calculates the Euclidean distance between this point and another point.

        Args:
            other (Coordinates): The other point.

        Returns:
            float: The distance between this point and the other point.

        Raises:
            ValueError: If the argument is not of type Coordinates.

        """
        if not isinstance(other, Coordinates):
            raise ValueError("Argument must be of type Coordinates.")
        x_diff = self.x - other.x
        y_diff = self.y - other.y
        return (x_diff**2 + y_diff**2) ** 0.5
