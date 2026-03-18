from math_core.sequence_calc import SequenceProcessor
from ui.console_input import get_integer_number
from ui.console_output import show_task_2_result

@show_task_2_result
def execute():
    """Выполнение второго задания - ввод, обработка, вывод"""

    print("\nЗадание 2")
    print("Вводите целые числа. Для завершения введите число больше 1000.")

    processor = SequenceProcessor()

    while True:
        num = get_integer_number("Введите число: ")

        if num >= 1000:
            break

        processor.add_number(num)

    return processor.get_result()
