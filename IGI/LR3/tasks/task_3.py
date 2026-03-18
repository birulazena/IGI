from ui.console_input import get_string_input
from text_core.text_analyzer import count_number_of_spaces

def execute():
    """Выполнение третьего заданияб - ввод, обработка, вывод"""

    print("\nЗадание 3")
    print("Подсчет колличества пробелов в тексте")

    user_text = get_string_input("Введите текс: ")

    number_of_spaces = count_number_of_spaces(user_text)

    print("\n--- РЕЗУЛЬТАТ ---")
    print(f"Количество пробелов: {number_of_spaces}")
    print("-" * 18)