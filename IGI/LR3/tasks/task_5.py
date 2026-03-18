from random import choice

from ui import console_input, console_output
from math_core import list_processor

def execute():
    """Выполнение пятого задание - ввод, обработка, вывод"""

    print("\nЗадание 5")

    print("1. Ввести числа самостоятельно")
    print("2. Сгенерировать числа")

    my_list = []

    while True:

        choice = input("Введите вариант создания: ")

        if choice == '1':
            my_list = console_input.get_float_list()
            break
        elif choice == '2':
            my_list = console_input.get_float_list_with_generator()
            break
        else:
            print("Ошибка: Неверный выбор варианта, попробуйте еще раз")


    print("Введенный вами список: ")
    print(my_list)

    print("\n--- РЕЗУЛЬТАТЫ ---")

    max_abs_idx = list_processor.find_max_abs_index(my_list)

    max_val = my_list[max_abs_idx]
    print(f"Максимальный по модулю элемент: {max_val} (его номер: {max_abs_idx})")

    mul = list_processor.calculate_mul_between_zeros(my_list)

    if mul is None:
        print("Произведение между двумя нулями вычислить невозможно. В списке меньше двух нулей")
    elif mul == 0.0:
        print("Нет элементов между двумя нулями")
    else:
        print(f"Произведение между двумя нулями: {mul}")

    print("-" * 18)

