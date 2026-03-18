from functools import wraps


def show_task_1_result(func):
    """Декоратор который отображает результат выполнения первого задания"""

    @wraps(func)
    def wrapper(*args, **kwargs):

        result = func(*args, **kwargs)

        if result is None:
            return None

        x, n, f_x, math_f_x, eps = result
        max_iter = 500

        print("\n" + "-" * 71)
        print(f"| {'x':^8} | {'n':^5} | {'F(x)':^15} | {'Math F(x)':^15} | {'eps':^10} |")
        print("-" * 71)
        print(f"| {x:^8} | {n:^5} | {f_x:^15.5f} | {math_f_x:^15.5f} | {eps:^10} |")
        print("-" * 71)

        return result
    return wrapper

def show_task_2_result(func):
    """Декоратор который отображает результат выполнения второго задания"""

    @wraps(func)
    def wrapper(*args, **kwargs):

        result = func(*args, **kwargs)

        if result is None:
            return None

        total_sum, even_count = result

        print("\n--- РЕЗУЛЬТАТЫ ---")
        print(f"Сумма всех введенных чисел: {total_sum}")
        print(f"Количество четных чисел: {even_count}")
        print("-" * 18)

        return result
    return wrapper

