import random
def find_max_abs_index(numbers: list) -> int:
    """Находит максимальное число по модулю из списка"""

    max_val = max(numbers, key=abs)

    return numbers.index(max_val)

def calculate_mul_between_zeros(numbers: list):
    """Считает произведение елементов между двумя нулями в списке"""

    try:
        first_zero = numbers.index(0.0)
        second_zero = numbers.index(0.0, first_zero + 1)

    except ValueError:
        return None

    if second_zero - first_zero <= 1:
        return 0.0

    mul = 1.0

    for i in range (first_zero + 1, second_zero):
        mul *= numbers[i]

    return mul

def randon_float_generator(count: int):
    """Выдает count случайных вещественных чисел"""
    for i in range(count):
        yield round(random.uniform(-10.0, 10.0), 2)
