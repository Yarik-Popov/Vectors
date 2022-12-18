from __future__ import annotations
import math
import turtle

# Constants
COLOURS_VECTORS = ['red', 'orange', 'green', 'blue', 'purple', 'violet']
COLOUR_AXES = 'grey'
COLOUR_VECTOR_RESULT = 'black'


class Vector2D:
    supported_types = (int, float)

    def __init__(self,
                 x: int | float = 0,
                 y: int | float = 0,
                 magnitude: int | float = 0,
                 angle: int | float = 0,
                 *, rounding_decimal=12):
        """
        This is a 2D vector class. It handles the storing and modifying of a vector.

        :param x: The x component
        :param y: The y component
        :param magnitude: The magnitude (If this is passed, it will create a vector using the magnitude and angle
        ignoring x, y)
        :param angle: The angle of the vector (This is only needed when the magnitude is passed in)
        :param rounding_decimal: How many decimals to round the other parameters in the vector
        """

        # Checks to make sure the parameters are valid types
        if not isinstance(x, self.supported_types) or not isinstance(y, self.supported_types) \
                or not isinstance(magnitude, self.supported_types) or not isinstance(angle, self.supported_types):
            raise TypeError(f'''{type(x) = } and {type(y) = } and {type(magnitude) = } and {type(angle) = }. All need \
to be int or float.''')

        # Initializes variables
        self.x = x
        self.y = y
        self.magnitude = magnitude
        self.angle = angle % 360
        self.angle_rad = math.radians(angle)
        self.rounding_decimal = rounding_decimal

        # Generates the x and y if the length is given, else it generates the length and angle
        if self.magnitude > 0:
            self.generate_x_y()
        elif self.magnitude < 0:
            self.angle += 180
            self.angle_rad = math.radians(self.angle)
            self.magnitude *= -1
            self.generate_x_y()
        else:
            self.generate_length_angle()

    def generate_x_y(self):
        """This method generates the x and y of the vector based on the angle_rad (radian of angle) and length"""
        self.x = round(self.magnitude * math.cos(self.angle_rad), self.rounding_decimal)
        self.y = round(self.magnitude * math.sin(self.angle_rad), self.rounding_decimal)

    def generate_length_angle(self):
        """This method generates the length and angle based on the x and y"""
        self.calculate_magnitude()

        # Calculates angle
        # Calculates if x is 0
        if not self.x:
            if self.y > 0:
                self.angle = 90
            elif self.y < 0:
                self.angle = 270
            else:
                self.angle = 0
            self.convert_to_radian_angle()

        # Calculates if x is not 0
        else:
            self.angle_rad = round(math.atan(self.y / self.x), self.rounding_decimal)
            self.angle = (math.degrees(self.angle_rad))

            # Makes sure the angle is positive
            if self.x < 0:
                self.angle += 180
            elif self.y < 0:
                self.angle += 360

    def convert_to_radian_angle(self):
        """Converts the angle from degrees to radians and sets it to the internal variable of self.angle_rad."""
        self.angle_rad = round(math.radians(self.angle), self.rounding_decimal)

    def calculate_magnitude(self):
        """Calculates the length of the vector based on the x and y components."""
        self.magnitude = round(math.sqrt(self.x ** 2 + self.y ** 2), self.rounding_decimal)

    def is_opposite(self, other):
        """Compares if 2 vectors are opposites to each other by comparing the x and y components"""
        if isinstance(other, Vector2D):
            return self.x == -other.x and self.y == -other.y

    def to_component_vectors(self):
        """Returns 2 vectors broken up into the original vector's x and y components"""
        return Vector2D(self.x), Vector2D(y=self.y)

    # Magic Methods

    def __eq__(self, other):
        if isinstance(other, Vector2D):
            return self.x == other.x and self.y == other.y
        raise TypeError

    def __neg__(self):
        return Vector2D(-self.x, -self.y)

    def __pow__(self, power, modulo=None):
        if isinstance(power, self.supported_types):
            if modulo is not None:
                return Vector2D(self.x ** power % modulo, self.y ** power % modulo)
            return Vector2D(self.x ** power, self.y ** power)

    def __sub__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x - other.x, self.y - other.y)

    def __isub__(self, other):
        if isinstance(other, Vector2D):
            self.x -= other.x
            self.y -= other.y
            self.generate_length_angle()
            return self
        raise TypeError(f'{type(other) = }. Must be of type Vector2D')

    def __add__(self, other):
        if isinstance(other, Vector2D):
            return Vector2D(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        if isinstance(other, Vector2D):
            self.x += other.x
            self.y += other.y
            self.generate_length_angle()
            return self
        raise TypeError(f'{type(other) = }. Other must be of type Vector2D')

    def __mul__(self, other):
        if isinstance(other, self.supported_types):
            return Vector2D(self.x * other, self.y * other)
        elif isinstance(other, Vector2D):
            return Vector2D(self.x * other.x, self.y * other.y)

    def __imul__(self, other):
        if isinstance(other, self.supported_types):
            self.x *= other
            self.y *= other
            self.calculate_magnitude()

            # Operations to be preformed if the other parameter is negative
            if other < 0:
                self.angle += 180

                if self.angle >= 360:
                    self.angle -= 360

                self.convert_to_radian_angle()

            return self

    def __truediv__(self, other):
        if isinstance(other, self.supported_types):
            return Vector2D(self.x / other, self.y / other)
        elif isinstance(other, Vector2D):
            return Vector2D(self.x / other.x, self.y / other.y)

    def __bool__(self):
        return self.magnitude != 0

    def __str__(self):
        return f'Vector ({self.x}, {self.y}) with magnitude: {self.magnitude} and angle: {self.angle}'

    def __repr__(self):
        return f'Vector2D(x={self.x}, y={self.y}, magnitude={self.magnitude}, angle={self.angle})'


def draw_axes(length: int | float = 400, color: str = COLOUR_AXES):
    """
    Draws the axes on the window

    :param length: Length of each axis
    :param color: Color of the axes
    :return:
    """
    turtle.pencolor(color)
    for i in range(4):
        turtle.forward(length)
        turtle.home()
        turtle.lt(90 * (i + 1))


def draw_vector(length: float | int, angle: float | int, *, back_to_east=True, scaling=1,
                arrow_decimal=0.1, arrow_angle: int | float = 30):
    """
    Draws the vector of the given length and angle to the right or east direction.

    :param length: Length of vector
    :param angle: Angle relative to east
    :param back_to_east: Returns the turtle back to facing east
    :param scaling: Scales the vector
    :param arrow_decimal: The decimal of how long the arrow of the vector will be
    :param arrow_angle: The angle the arrows will make with the original line
    :return:
    """

    # Draw vector
    turtle.lt(angle)
    turtle.forward(length * scaling)

    # Draw the arrows
    arrow_length = length * scaling * arrow_decimal

    # Draw the left arrow
    turtle.lt(arrow_angle)
    draw_back_forward(arrow_length)

    # Draw the right arrow
    turtle.rt(2 * arrow_angle)
    draw_back_forward(arrow_length)
    turtle.lt(arrow_angle)

    # Return the turtle back to the east
    if back_to_east:
        turtle.rt(angle)


def draw_back_forward(length: int | float):
    """Moves the turtle back and forward a set length. Used in the draw_vectors() function"""
    turtle.back(length)
    turtle.forward(length)


def draw_vectors(*vectors: list | Vector2D):
    """
    Draws the list of Vector2D objects to a turtle window, adds the vectors together and returns it. Returns None if
    there are no vectors

    :param vectors: List of Vector2D objects
    :return: Result Vector or None
    """
    # Make sure the method can generate vectors
    if not vectors or len(vectors) == 1 and not vectors[0]:
        return

    # Allows the user to insert a list instead of a tuple
    if len(vectors) == 1 and isinstance(vectors[0], list):
        vectors = vectors[0]

    # Makes sure the turtle is in the proper position each time
    turtle.TurtleScreen._RUNNING = True
    turtle.home()
    turtle.clear()

    # Initialize important variables
    vector_result = Vector2D()
    canvas_width, canvas_height = turtle.screensize()
    x_min = x_max = y_min = y_max = 0
    x_scaling = y_scaling = 1

    for i in vectors:
        # Adds to vector result, gets x and y of it
        vector_result += i
        x = vector_result.x
        y = vector_result.y

        # Sets the boundaries
        if x_min > x:
            x_min = x
        elif x_max < x:
            x_max = x
        if y_min > y:
            y_min = y
        elif y_max < y:
            y_max = y

    # Creates scaling
    x_range = x_max - x_min
    y_range = y_max - y_min

    # Makes sure not to divide by 0
    if x_range:
        x_scaling = canvas_width / x_range
    if y_range:
        y_scaling = canvas_height / y_range

    scaling = min(x_scaling, y_scaling)

    # Edge case checking for scaling
    if x_range and not y_range:
        scaling = x_scaling
    elif y_range and not x_range:
        scaling = y_scaling

    draw_axes(max(canvas_width, canvas_height))

    # Loop over the vectors and draw them
    for i, value in enumerate(vectors):
        turtle.pencolor(COLOURS_VECTORS[i % len(COLOURS_VECTORS)])
        draw_vector(value.magnitude, value.angle, scaling=scaling)

    # Draw result vector
    turtle.pencolor(COLOUR_VECTOR_RESULT)
    turtle.home()
    draw_vector(vector_result.magnitude, vector_result.angle, back_to_east=False, scaling=scaling)
    return vector_result


def is_float(value: str):
    """
    A function to check if the given string named value is a float \n
    >>> is_float('3')
    True
    >>> is_float('-0.1')
    True
    >>> is_float('3.3.3')
    False
    >>> is_float('A three')
    False
    """
    try:
        float(value)
        return True
    except ValueError:
        return False
