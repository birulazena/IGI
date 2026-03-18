import math

def calculate_ln_series(x: float, eps: float, max_iter: int = 500) -> tuple:
    """Считает функцию при помощи ряда тейлора"""

    n = 1
    term = -x
    f_x = 0.0

    while abs(term) >= eps and n <= max_iter:
        f_x += term
        n += 1
        term = term * x * (n - 1) / n

    return f_x, n - 1

def get_exact_ln_values(x: float) -> float:
    """Считает функцию при попощи встроенных методов"""

    return math.log(x)