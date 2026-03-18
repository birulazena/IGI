# =========================================================
# Laboratory Work #3
# Student: Birylia Yauheni
# Date: 18.03.2026
# =========================================================

# This laboratory work consists of 5 tasks:

# Task 1: Calculate a function using Taylor series expansion.
# Task 2: Calculate the sum and count the number of even numbers in a sequence.
# Task 3: Count the number of spaces in the input string.
# Task 4: Count the words, find the shortest word ending in 'd',
#         and sort the words in descending order.
# Task 5: Find the maximum absolute value and calculate the product
#         of elements located between two zeros.

# =========================================================


import os
import tasks


def main():

    while True:
        print("\n1. Задание 1 (Ряд Тейлора)")
        print("2. Задание 2 (Сумма последовательности чисел)")
        print("3. Задание 3 (Анализ текста с клавиатуры)")
        print("4. Задание 4 (Анализ заданного текста)")
        print("5. Задание 5 (Обработка вещественных чисел)")
        print("0. Выход")

        choice = input("Выберите номер задания: ")

        if choice == '1':
            tasks.task_1.execute()
        elif choice == '2':
            tasks.task_2.execute()
        elif choice == '3':
            tasks.task_3.execute()
        elif choice == '4':
            tasks.task_4.execute()
        elif choice == '5':
            tasks.task_5.execute()
        elif choice == '0':
            print("\nРабота программы завершена")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == '__main__':
    main()
