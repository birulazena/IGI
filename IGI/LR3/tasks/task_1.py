from ui.console_output import show_task_1_result
from ui import console_input
from math_core import taylor_series

@show_task_1_result
def execute():
    """Выполнение первого задание - ввод, обработка, вывод"""

    print("\nЗадание 1")

    x, eps = console_input.get_task_1_parameters()

    f_x, n = taylor_series.calculate_ln_series(x, eps)
    math_f_x = taylor_series.get_exact_ln_values(x)

    return x, n, f_x, math_f_x, eps