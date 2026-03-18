class SequenceProcessor:
    """Считает колличество четных чисел, а так же суммируется все числа,
    которые попадают в метод add_number"""

    def __init__(self):
        self.even_count = 0
        self.total_sum = 0

    def add_number(self, number: int):
        """Добавляет число к сумме и увеличивает счетки четных числел,
        если принятое число четное"""

        self.total_sum += number

        if number % 2 == 0:
            self.even_count += 1

    def get_result(self) -> tuple:
        """Отдает результат в виде кортеджа"""

        return self.total_sum, self.even_count
