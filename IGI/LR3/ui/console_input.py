from itertools import count
from math_core.list_processor import randon_float_generator


def get_task_1_parameters() -> tuple:
    """Получение данных для первого задания из консоли"""

    while True:
        try:
            x_input = input("Введите значение x (|x| < 1): ")
            x = float(x_input)

            if abs(x) >= 1:
                raise ValueError(f"Число x не входит в интервал (-1, 1)")

            eps_input = input("Введите точность eps: ")
            eps = float(eps_input)

            if eps <= 0:
                raise ValueError("Точность должна быть положительным числом")

            return x, eps

        except ValueError as e:
            print(f"\nОшибка ввода: {e}")
            print("Введите данные еще раз\n")

def get_integer_number(prompt_text: str) -> int:
    """Получение целого числа из консоли"""

    while True:
        try:
            user_input = input(prompt_text)
            return int(user_input)
        except ValueError:
            print("Ошибка, введите целое число")

def get_string_input(prompt_text: str) -> str:
    """Получение строки"""

    return input(prompt_text)

def get_float_list() -> list:
    """Получение вещественного списка"""

    while True:
        try:
            count = int(input("Введите количество элементов списка: "))
            if count <= 0:
                print("Ошибка: Список должен содержать хотя бы 1 элемент.")
                continue
            break
        except ValueError:
            print("Ошибка: Введите целое положительное число")

    result_list = []
    print("\nВводите вещественные числа:")

    for i in range(count):
        while True:
            try:
                value = float(input(f"Элемент {i}: "))
                result_list.append(value)
                break
            except ValueError:
                print("Ошибка: Введено не вещественное число. Попробуйте еще раз")

    return result_list


def get_float_list_with_generator() -> list:
    """Получение вещественного списка при помощи генератора"""

    while True:
        try:
            count = int(input("Сколько чисел сгенерировать? "))
            if count <= 0:
                print("Ошибка: Список должен содержать хотя бы 1 элемент.")
                continue
            break
        except ValueError:
            print("Ошибка: Введите положительное число.")

    result_list = []

    for value in randon_float_generator(count):
        result_list.append(value)

    return result_list