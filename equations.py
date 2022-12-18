from __future__ import annotations
# Equations used in the vectors program
import support
from support import Vector2D
import math

EQUATIONS = (('Vi = d/t - A*t/2', 'Vi = 2d/t - Vf', 'Vi = A*t - Vf', 'Vi = sqrt(Vf^2 - 2A*d)'),
             ('Vf = d/t + A*t/2', 'Vf = 2d/t - Vi', 'Vf = Vi + A*t', 'Vf = sqrt(Vi^2 + 2A*d)'),
             ('A = 2Vf/t - 2d/(t^2)', 'A = 2d/(t^2) - 2Vi/t', 'A = Vf/t - Vi/t', 'A = (Vf^2 - Vi^2)/2d'),
             ('d = Vf*t - A*(t^2)/2', 'd = Vi*t + A*(t^2)/2', 'd = Vf*t/2 + Vi*t/2', 'd = (Vf^2)/2A - (Vi^2)/2A'),
             ('t = (Vf -+ sqrt(Vf^2 - 2A*d))/A', 't = (-Vi -+ sqrt(Vi^2 + 2A*d))/A', 't = 2d/(Vf + Vi)',
              't = Vf/A - Vi/A'))


def calculate_vi_no_vf(acceleration: Vector2D, displacement: Vector2D, time: int | float, *, draw_vectors=True) \
        -> Vector2D:
    """
    Calculates the initial velocity of an object based on the displacement, acceleration and time. Draws on a turtle the
    calculations used and returns the initial velocity. Draws d/t then -A*t/2

    Equation: Vi = d/t - A*t/2

    :param displacement: Displacement of object (d)
    :param acceleration: Acceleration of object (A)
    :param time: Time the object is in motion (t)
    :param draw_vectors: Draws the vectors on a turtle window. Default is True
    """
    d = displacement / time
    a = -acceleration * time / 2
    vi = d + a
    if draw_vectors:
        support.draw_vectors(d, a)
    return vi


def calculate_vi_no_a(velocity_final: Vector2D, displacement: Vector2D, time: int | float, *, draw_vectors=True) \
        -> Vector2D:
    """
    Calculates the initial velocity of an object based on the final velocity, displacement and time. Draws the
    calculates used on a turtle. Then returns the initial velocity. Draws 2d/t then -Vf

    Equation: Vi = 2d/t - Vf

    :param velocity_final: Final velocity of an object (Vf)
    :param displacement: Displacement of an object (d)
    :param time: Time of flight of an object (t)
    :param draw_vectors: Draws the vectors on a turtle window. Default is True
    :return: Initial Velocity (Vi)
    """
    d = displacement * (2/time)
    vf = -velocity_final
    vi = d + vf
    if draw_vectors:
        support.draw_vectors(d, vf)
    return vi


def calculate_vi_no_d(velocity_final: Vector2D, acceleration: Vector2D, time: int | float, *, draw_vectors=True) \
        -> Vector2D:
    """
    Calculates the initial velocity of an object based on the final velocity, acceleration and time. Draws on a turtle
    the calculations used and returns the initial velocity. Draws A*t then -Vf

    Equation: Vi = A*t - Vf

    :param velocity_final: Final velocity of an object (Vf)
    :param acceleration: Acceleration of an object (A)
    :param time: Time the object is in motion (t)
    :param draw_vectors: Draws the vectors on a turtle window. Default is True
    :return: Initial Velocity (Vi)
    """
    a = acceleration * time
    vf = - velocity_final
    vi = a + vf
    if draw_vectors:
        support.draw_vectors(a, vf)
    return vi


def calculate_vi_no_t(velocity_final: Vector2D, acceleration: Vector2D, displacement: Vector2D) \
        -> float:
    """
    Calculates the initial velocity of an object based on the final velocity, acceleration and displacement. Doesn't
    draw on a turtle the calculations used. Returns the magnitude of the initial velocity.

    Equation: Vi = sqrt(Vf^2 - 2A*d)

    :param velocity_final: Final velocity of an object (Vf)
    :param acceleration: Acceleration of object (A)
    :param displacement: Displacement of object (d)
    :return: Magnitude of Initial Velocity (Vi)
    """
    return math.sqrt(velocity_final.magnitude ** 2 - calculate_2_a_d(acceleration, displacement))


def calculate_vf_no_vi(acceleration: Vector2D, displacement: Vector2D, time: int | float, *, draw_vectors=True) \
        -> Vector2D:
    """
    Calculates the final velocity of an object based on the acceleration, displacement and time. Draws on a
    turtle the calculations used and returns the final velocity. Draws d/t then A*t/2

    Equation: Vf = d/t + A*t/2

    :param acceleration: Acceleration of object (A)
    :param displacement: Displacement of object (d)
    :param time: Time the object is in motion (t)
    :param draw_vectors: Draws the vectors on a turtle window. Default is True
    :return: Final velocity of an object (Vf)
    """
    d = displacement / time
    a = acceleration * time / 2
    vf = d + a
    if draw_vectors:
        support.draw_vectors(d, a)
    return vf


def calculate_vf_no_a(velocity_initial: Vector2D, displacement: Vector2D, time: int | float, *, draw_vectors=True) \
        -> Vector2D:
    """
    Calculates the final velocity of an object based on the initial velocity, displacement and time. Draws on a
    turtle the calculations used and returns the final velocity. Draws 2d/t then Vi

    Equation: Vf = 2d/t - Vi

    :param velocity_initial: Initial Velocity (Vi)
    :param displacement: Displacement of object (d)
    :param time: Time the object is in motion (t)
    :param draw_vectors: Draws the vectors on a turtle window. Default is True
    :return: Final velocity of an object (Vf)
    """
    d = displacement * 2 / time
    vi = - velocity_initial
    vf = d + vi
    if draw_vectors:
        support.draw_vectors(d, vi)
    return vf


def calculate_vf_no_d(velocity_initial: Vector2D, acceleration: Vector2D, time: int | float, *, draw_vectors=True) \
        -> Vector2D:
    """
    Calculates the final velocity of an object based on the initial velocity, acceleration and time. Draws on a
    turtle the calculations used and returns the final velocity. Draws Vi then A*t

    Equation: Vf = Vi + A*t

    :param velocity_initial: Initial Velocity (Vi)
    :param acceleration: Acceleration of object (A)
    :param time: Time the object is in motion (t)
    :param draw_vectors: Draws the vectors on a turtle window. Default is True
    :return: Final velocity of an object (Vf)
    """
    a = acceleration * time
    vf = velocity_initial + a
    if draw_vectors:
        support.draw_vectors(velocity_initial, a)
    return vf


def calculate_vf_no_t(velocity_initial: Vector2D, acceleration: Vector2D, displacement: Vector2D)\
        -> float:
    """
    Calculates the final velocity of an object based on the initial velocity, acceleration, and displacement. Doesn't
    draw on a turtle the calculations used. Returns the magnitude of the final velocity.

    Equation: Vf = sqrt(Vi^2 + 2A*d)

    :param velocity_initial: Initial Velocity (Vi)
    :param acceleration: Acceleration of object (A)
    :param displacement: Displacement of object (d)
    :return: Final velocity of an object (Vf)
    """
    return math.sqrt(velocity_initial.magnitude ** 2 + calculate_2_a_d(acceleration, displacement))


def calculate_a_no_vi(velocity_final: Vector2D, displacement: Vector2D, time: int | float, *, draw_vectors=True) \
        -> Vector2D:
    """
    Calculates the acceleration of an object based on the final velocity, displacement and time. Draws on a
    turtle the calculations used and returns the acceleration. Draws 2Vf/t then -2d/(t^2)

    Equation: A = 2Vf/t - 2d/(t^2)

    :param velocity_final: Final velocity of an object (Vf)
    :param displacement: Displacement of object (d)
    :param time: Time the object is in motion (t)
    :param draw_vectors: Draws the vectors on a turtle window. Default is True
    :return: Acceleration of object (A)
    """
    vf = velocity_final * 2 / time
    d = -displacement * 2 / (time ** 2)
    a = vf + d
    if draw_vectors:
        support.draw_vectors(vf, d)
    return a


def calculate_a_no_vf(velocity_initial: Vector2D, displacement: Vector2D, time: int | float, *, draw_vectors=True) \
        -> Vector2D:
    """
    Calculates the acceleration of an object based on the initial velocity, displacement and time. Draws on a
    turtle the calculations used and returns the acceleration. Draws 2d/(t^2) then 2Vi/t

    Equation: A = 2d/(t^2) - 2Vi/t

    :param velocity_initial: Initial Velocity (Vi)
    :param displacement: Displacement of object (d)
    :param time: Time the object is in motion (t)
    :param draw_vectors: Draws the vectors on a turtle window. Default is True
    :return: Acceleration of object (A)
    """
    d = displacement * 2 / (time ** 2)
    vi = -velocity_initial * 2 / time
    a = d + vi
    if draw_vectors:
        support.draw_vectors(d, vi)
    return a


def calculate_a_no_d(velocity_initial: Vector2D, velocity_final: Vector2D, time: int | float, *, draw_vectors=True) \
        -> Vector2D:
    """
    Calculates the acceleration of an object based on the initial velocity, final velocity and time. Draws on a
    turtle the calculations used and returns the acceleration. Draws Vf/t then -Vi/t

    Equation: A = Vf/t - Vi/t

    :param velocity_initial: Initial Velocity (Vi)
    :param velocity_final: Final velocity of an object (Vf)
    :param time: Time the object is in motion (t)
    :param draw_vectors: Draws the vectors on a turtle window. Default is True
    :return: Acceleration of object (A)
    """
    vf = velocity_final / time
    vi = -velocity_initial / time
    a = vf + vi
    if draw_vectors:
        support.draw_vectors(vf, vi)
    return a


def calculate_a_no_t(velocity_initial: Vector2D, velocity_final: Vector2D, displacement: Vector2D, *,
                     draw_vectors=True) -> Vector2D:
    """
    Calculates the acceleration of an object based on the initial velocity, final velocity and displacement. Draws on a
    turtle the calculations used and returns the acceleration.

    Equation: A = (Vf^2)/2d - (Vi^2)/2d

    :param velocity_initial: Initial Velocity (Vi)
    :param velocity_final: Final velocity of an object (Vf)
    :param displacement: Displacement of object (d)
    :param draw_vectors: Draws the vectors on a turtle window. Default is True
    :return: Acceleration of object (A)
    """
    vf = velocity_final ** 2 / (displacement * 2)
    vi = -(velocity_initial ** 2) / (displacement * 2)
    a = vf + vi
    if draw_vectors:
        support.draw_vectors(vf, vi)
    return a


def calculate_d_no_vi(velocity_final: Vector2D, acceleration: Vector2D, time: int | float, *, draw_vectors=True) \
        -> Vector2D:
    """
    Calculates the displacement of an object based on the final velocity, acceleration and time. Draws on a
    turtle the calculations used and returns the displacement. Draws Vf*t then -A*(t^2)/2

    Equation: d = Vf*t - A*(t^2)/2

    :param velocity_final: Final velocity of an object (Vf)
    :param acceleration: Acceleration of object (A)
    :param time: Time the object is in motion (t)
    :param draw_vectors: Draws the vectors on a turtle window. Default is True
    :return: Displacement of object (d)
    """
    vf = velocity_final * time
    a = -acceleration * (time**2)/2
    d = vf + a
    if draw_vectors:
        support.draw_vectors(vf, a)
    return d


def calculate_d_no_vf(velocity_initial: Vector2D, acceleration: Vector2D, time: int | float, *, draw_vectors=True) \
        -> Vector2D:
    """
    Calculates the displacement of an object based on the initial velocity, acceleration and time. Draws on a
    turtle the calculations used and returns the displacement. Draws Vi*t then A*(t^2)/2

    Equation: d = Vi*t + A*(t^2)/2

    :param velocity_initial: Initial Velocity (Vi)
    :param acceleration: Acceleration of object (A)
    :param time: Time the object is in motion (t)
    :param draw_vectors: Draws the vectors on a turtle window. Default is True
    :return: Displacement of object (d)
    """
    vi = velocity_initial * time
    a = acceleration * (time ** 2)/2
    d = vi + a
    if draw_vectors:
        support.draw_vectors(vi, a)
    return d


def calculate_d_no_a(velocity_initial: Vector2D, velocity_final: Vector2D, time: int | float, *, draw_vectors=True) \
        -> Vector2D:
    """
    Calculates the displacement of an object based on the initial velocity, final velocity and time. Draws on a
    turtle the calculations used and returns the displacement. Draws Vf*t/2 then Vi*t/2

    Equation: d = Vf*t/2 + Vi*t/2

    :param velocity_initial: Initial Velocity (Vi)
    :param velocity_final: Final velocity of an object (Vf)
    :param time: Time the object is in motion (t)
    :param draw_vectors: Draws the vectors on a turtle window. Default is True
    :return: Displacement of object (d)
    """
    vf = velocity_final * time / 2 
    vi = velocity_initial * time / 2
    d = vf + vi
    if draw_vectors:
        support.draw_vectors(vf, vi)
    return d


def calculate_d_no_t(velocity_initial: Vector2D, velocity_final: Vector2D, acceleration: Vector2D, *,
                     draw_vectors=True) -> Vector2D:
    """
    Calculates the displacement of an object based on the initial velocity, final velocity and acceleration. Draws on a
    turtle the calculations used and returns the displacement.

    Equation: d = (Vf^2)/2A - (Vi^2)/2A

    :param velocity_initial: Initial Velocity (Vi)
    :param velocity_final: Final velocity of an object (Vf)
    :param acceleration: Acceleration of object (A)
    :param draw_vectors: Draws the vectors on a turtle window. Default is True
    :return: Displacement of object (d)
    """
    vf = (velocity_final ** 2) / (acceleration * 2)
    vi = -(velocity_initial ** 2) / (acceleration * 2)
    d = vf + vi
    if draw_vectors:
        support.draw_vectors(vf, vi)
    return d


def calculate_t_no_vi(velocity_final: int | float, acceleration: int | float, displacement: int | float):
    """
    Calculates the time of flight of an object based on the final velocity, acceleration and displacement returns the
    time.

    Equation: t = (Vf -+ sqrt(Vf^2 - 2A*d))/A

    :param velocity_final: Final velocity of an object (Vf)
    :param acceleration: Acceleration of object (A)
    :param displacement: Displacement of object (d)
    :return: Time the object is in motion (t)
    """
    return solve_quadratic_equation(acceleration / 2, -velocity_final, displacement)


def calculate_t_no_vf(velocity_initial: int | float, acceleration: int | float, displacement: int | float):
    """
    Calculates the time of flight of an object based on the initial velocity, acceleration and displacement returns the
    time.

    Equation: t = (-Vi -+ sqrt(Vi^2 + 2A*d))/A

    :param velocity_initial: Initial Velocity (Vi)
    :param acceleration: Acceleration of object (A)
    :param displacement: Displacement of object (d)
    :return: Time the object is in motion (t)
    """
    return solve_quadratic_equation(acceleration / 2, velocity_initial, -displacement)


def calculate_t_no_a(velocity_initial: Vector2D, velocity_final: Vector2D, displacement: Vector2D):
    """
    Calculates the time of flight of an object based on the initial velocity, final velocity and displacement returns 
    the time.

    Equation: t = 2d/(Vf + Vi)

    :param velocity_initial: Initial Velocity (Vi)
    :param velocity_final: Final velocity of an object (Vf)
    :param displacement: Displacement of object (d)
    :return: Time the object is in motion (t)
    """
    return 2 * displacement.magnitude / (velocity_final.magnitude + velocity_initial.magnitude)


def calculate_t_no_d(velocity_initial: Vector2D, velocity_final: Vector2D, acceleration: Vector2D):
    """
    Calculates the time of flight of an object based on the initial velocity, final velocity and acceleration and
    returns the time.

    Equation: t = (Vf - Vi)/A

    :param velocity_initial: Initial Velocity (Vi)
    :param velocity_final: Final velocity of an object (Vf)
    :param acceleration: Acceleration of object (A)
    :return: Time the object is in motion (t)
    """
    return (velocity_final.magnitude - velocity_initial.magnitude) / acceleration.magnitude


def solve_quadratic_equation(a: int | float, b: int | float, c: int | float) \
        -> tuple | tuple[float] | tuple[float, float]:
    """
    Solves the quadratic equation using the quadratic formula.

    Standard form: 0 = ax^2 + bx + c

    Formula: x = (-b -+ sqrt(b^2 - 4a*c))/2a

    >>> solve_quadratic_equation(0, 1, 2)
    (-2.0,)

    >>> solve_quadratic_equation(0, 2, 0)
    (0.0,)

    >>> solve_quadratic_equation(1, -1, -6)
    (3.0, -2.0)

    >>> solve_quadratic_equation(1, 2, 2)
    ()

    >>> solve_quadratic_equation(1, -5, 5)
    (3.618033988749895, 1.381966011250105)

    >>> solve_quadratic_equation(0, 0, 2)
    ()

    >>> solve_quadratic_equation(0, 0, 0)
    (-inf, inf)

    :param a: Coefficient on x^2 (If a = 0 and b != 0 then uses x = -c/b)
    :param b: Coefficient on x
    :param c: Intercept when x = 0
    :return: x1, x2
    """
    # A line is inputted
    if not a:
        if b:
            return -c / b,
        if not c:
            return -math.inf, math.inf
        return tuple()

    # Make sure the inside of square root is real, if not return a tuple
    inside = b**2 - 4*a*c
    if inside < 0:
        return tuple()

    # Calculate x1, x2
    x1 = (-b + math.sqrt(inside))/(2*a)
    x2 = (-b - math.sqrt(inside))/(2*a)
    return x1, x2


def calculate_2_a_d(acceleration: Vector2D, displacement: Vector2D) -> float:
    """
    Used in the calculate_vi_no_t() and calculate_vf_no_t()

    :param acceleration: Acceleration of object
    :param displacement: Displacement of object
    :return: 2 * acceleration.magnitude * displacement.magnitude
    """
    return 2 * acceleration.magnitude * displacement.magnitude
